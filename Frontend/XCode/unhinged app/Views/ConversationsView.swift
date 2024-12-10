//
//  ConversationsView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//

import Foundation
import SwiftUI
import SwiftData

public struct ConversationsView: View {
    
    @EnvironmentObject var appModel: AppModel
    
    public var body: some View {
        List{
            
           
            
        }
    }
    
    private func getConversations() -> [Conversation] {
        
        
        return []
        
    }
    
}


#Preview {
    ConversationsView()
}
