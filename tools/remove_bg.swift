// Remove the background from a photo using macOS's built-in subject lifting (Vision).
// macOS 14 or newer. No downloads, no account, runs on your Mac.
//
// Usage:  swift tools/remove_bg.swift input.jpg output.png [--all]
//   --all  keep every subject Vision finds (default keeps all foreground instances too;
//          pass instance numbers instead, e.g. "1,2", to keep only some)
// Output: a PNG with a transparent background, cropped to the subject.
import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("Usage: swift remove_bg.swift input.jpg output.png [1,2]"); exit(2)
}
let inURL = URL(fileURLWithPath: args[1]), outURL = URL(fileURLWithPath: args[2])
guard let src = CGImageSourceCreateWithURL(inURL as CFURL, nil),
      let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("Cannot read \(args[1])"); exit(1) }

let req = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
do { try handler.perform([req]) } catch { print("Vision failed: \(error)"); exit(1) }
guard let obs = req.results?.first else { print("No subject found."); exit(1) }

var keep = obs.allInstances
if args.count >= 4, args[3] != "--all" {
    keep = IndexSet(args[3].split(separator: ",").compactMap { Int($0) })
}
print("Subjects found: \(obs.allInstances.count). Keeping: \(Array(keep))")
do {
    let buf = try obs.generateMaskedImage(ofInstances: keep, from: handler, croppedToInstancesExtent: true)
    let ci = CIImage(cvPixelBuffer: buf)
    let ctx = CIContext()
    guard let out = ctx.createCGImage(ci, from: ci.extent, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!) else { exit(1) }
    guard let dst = CGImageDestinationCreateWithURL(outURL as CFURL, UTType.png.identifier as CFString, 1, nil) else { exit(1) }
    CGImageDestinationAddImage(dst, out, nil)
    CGImageDestinationFinalize(dst)
    print("Saved \(args[2]) (\(out.width) x \(out.height))")
} catch { print("Mask failed: \(error)"); exit(1) }
