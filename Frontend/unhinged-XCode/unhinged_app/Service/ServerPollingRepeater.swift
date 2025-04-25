//
//  ServerPollingRepeater.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/23/25.
//

import Foundation
import SwiftUI

@MainActor
class ServerPollingRepeater : ObservableObject {
    
    private var task: Task<Void, Never>?
    private static var isRunning: Bool = false
    
    @Published var didDetectNewMessages: Bool = false
    @Published var didDetectNewMatches: Bool = false

    func start() {
        print("MESSAGE/MATCH POLLING STARTED")
        if !ServerPollingRepeater.isRunning {
            ServerPollingRepeater.isRunning = true
            task = Task {
                while !Task.isCancelled {
                    print("POLLING FOR NEW MATCHES AND MESSAGES")
                    didDetectNewMessages =  await APIClient.shared.pollMessages()
                    didDetectNewMessages = await APIClient.shared.pollMatches()
                    try? await Task.sleep(nanoseconds: 10 * 1_000_000_000)
                    didDetectNewMatches = false
                    didDetectNewMessages = false
                }
            }
        }
    }

    func stop() {
        task?.cancel()
        ServerPollingRepeater.isRunning = false
    }
}
