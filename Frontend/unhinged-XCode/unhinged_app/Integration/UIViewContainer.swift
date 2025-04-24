//
//  UIViewContainer.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/20/25.
//


import SwiftUI
import UIKit

struct UIViewContainer: UIViewRepresentable {
    
    var view: UIView
    
    func makeUIView(context: Context) -> UIView {
        return view
    }

    func updateUIView(_ uiView: UIView, context: Context) {
        // Update logic if needed
    }
}
