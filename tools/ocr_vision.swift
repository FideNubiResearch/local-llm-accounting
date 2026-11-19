// Apple Vision OCR of page images (offline): prints "=== <path>" then "<top> <left>\t<text>" per line.
// Used by tools/mask_probe_scan.py.  swiftc -O tools/ocr_vision.swift -o <scratch>/ocr_vision

import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("ERR \(path)"); continue }
  let req = VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.usesLanguageCorrection = false
  let h = VNImageRequestHandler(cgImage: cg, options: [:])
  try? h.perform([req])
  print("=== \(path)")
  for o in (req.results ?? []) { if let t = o.topCandidates(1).first { let b=o.boundingBox; print(String(format:"%.3f %.3f\t", 1-b.origin.y-b.height, b.origin.x) + t.string) } }
}
