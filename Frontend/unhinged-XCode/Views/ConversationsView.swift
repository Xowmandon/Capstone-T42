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
    
    @State private var conversations : [Conversation]
    
    init(){
        self.conversations = [Conversation(), Conversation()]
    }
    
    @ViewBuilder
    func conversationRow(conversation: Conversation) -> some View {
        
        NavigationLink(destination: MessageView(profile: conversation.with)){
            
            HStack{
                
                Image(conversation.with.imageName)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: 50, height: 50)
                    .clipShape(Circle())
                    .shadow(radius: 3)
                
                VStack {
                    
                    Text(conversation.with.name)
                        .bold()
                    
                    Text(conversation.messages.last?.content ?? "No Messages")
                        .font(.footnote)
                        .padding(.horizontal)
                }
                .frame(alignment: .topLeading)
                
            
            }
            
        }
        
        
    }
    
    public var body: some View {
        List(conversations){conversation in
            
            conversationRow(conversation: conversation)
            
        }
    }
    
    private func getConversations() -> [Conversation] {
        
        
        return []
        
    }
    
}


#Preview {
    NavigationStack{
        ConversationsView()
    }
}
