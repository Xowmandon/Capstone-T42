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
        self.conversations = [Conversation(), Conversation(), Conversation()]
    }
    
    @ViewBuilder
    func conversationRow(conversation: Conversation) -> some View {
        
        NavigationLink(destination: MessageView(profile: conversation.recipient)){
            
            HStack{
                
                Image(conversation.recipient.imageName)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: 50, height: 50)
                    .clipShape(Circle())
                    .shadow(radius: 3)
                    .padding()
                
                VStack (spacing: 5){
                    
                    Text(conversation.recipient.name)
                        .font(Theme.headerFont)
                        .bold()
                    
                    Text(conversation.messages.last?.content ?? "No Messages")
                        .font(Theme.bodyFont)
                        .padding(.leading, 5)
                }
                .frame(alignment: .topLeading)
                .padding()   
            
            }
            .background{
                
                CardBackground(borderColor: Theme.defaultBorderColor, innerColor: Theme.defaultInnerColor)
                
            }
            
        }
        
        
    }
    
    public var body: some View {
        List(conversations){conversation in
            
            conversationRow(conversation: conversation)
            
        }
    }
    
    // Query database for conversations associated with client account
    private func getConversations() -> [Conversation] {
        
        return []
        
    }
    
}


#Preview {
    NavigationStack{
        ConversationsView()
    }
}
