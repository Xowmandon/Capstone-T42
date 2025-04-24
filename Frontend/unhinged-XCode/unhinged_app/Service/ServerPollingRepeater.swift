//
//  ServerPollingRepeater.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/23/25.
//

import Foundation
import SwiftUI

class ServerPollingRepeater {
    private var task: Task<Void, Never>?

    func start() {
        task = Task {
            while !Task.isCancelled {
                //APIClient.shared.fetchLatestData()
                try? await Task.sleep(nanoseconds: 5 * 1_000_000_000)
            }
        }
    }

    func stop() {
        task?.cancel()
    }
}
