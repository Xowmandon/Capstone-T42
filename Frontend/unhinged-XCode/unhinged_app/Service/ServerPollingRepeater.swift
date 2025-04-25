//
//  ServerPollingRepeater.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/23/25.
//

import Foundation
import SwiftUI

class ServerPollingRepeater : ObservableObject {
    
    private var task: Task<Void, Never>?
    
    @Published var didDetectNewMessages: Bool = false
    @Published var didDetectNewMatches: Bool = false

    func start() {
        print("MESSAGE/MATCH POLLING STARTED")
        task = Task {
            while !Task.isCancelled {
                print("POLLING FOR NEW MATCHES AND MESSAGES")
                //APIClient.shared.fetchLatestData()
                didDetectNewMessages =  await APIClient.shared.pollMessages()
                didDetectNewMessages = await APIClient.shared.pollMatches()
                try? await Task.sleep(nanoseconds: 5 * 1_000_000_000)
            }
        }
    }

    func stop() {
        task?.cancel()
    }
}
