//
//  AppModel.swift
//  unhinged app
//
//  Created by Harry Sho on 12/8/24.
//

import Foundation
import SwiftUI

final class AppModel : ObservableObject {
    
    var prospectiveMatches : [Profile]
    
    var conversations : [Conversation]
    
    init() {
        self.prospectiveMatches = []
        self.conversations = []
    }
    
}
