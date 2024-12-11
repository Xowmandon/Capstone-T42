//
//  AppModel.swift
//  unhinged app
//
//  Created by Harry Sho on 12/8/24.
//

import Foundation
import SwiftUI

final class AppModel : ObservableObject {
    
    @Published var prospectiveMatches : [Profile]
    
    var conversations : [Conversation]
    
    init() {
        self.prospectiveMatches = [Profile(), Profile(name: "john doe1", imageName: "stockPhoto"), Profile(name: "john doe2", imageName: "stockPhoto")]
        self.conversations = []
    }
    
}
