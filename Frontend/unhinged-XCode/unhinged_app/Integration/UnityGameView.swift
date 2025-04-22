//
//  UnityGameView.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/20/25.
//


import Foundation
import SwiftUI



struct UnityGameView: View {
    private var unity = Unity.shared
    //@ObservedObject private var proxy : NativeCallProtocol
    @State private var loading : Bool = false
    
    var body: some View {
        ZStack {
            if loading {
                // Unity is starting up or shutting down
                ProgressView("Loading...").foregroundStyle(.primary)
            } else if let UnityContainer = unity.view.flatMap({ UIViewContainer(view: $0) }) {
                UnityContainer
            } else {
                Button("Start Unity", systemImage: "play", action: {
                    /* Unity startup is slow and must must occur on the
                     main thread. Use async dispatch so we can re-render
                     with a ProgressView before the UI becomes unresponsive. */
                    loading = true
                    DispatchQueue.main.async(execute: {
                        unity.start()
                        loading = false
                    })
                })
            }
        }
    }
}
