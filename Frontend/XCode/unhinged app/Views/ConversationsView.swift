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
            
            VStack(alignment: .leading){
                HStack{
                    conversation.recipient.image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 70, height: 70)
                        .clipShape(Circle())
                        .shadow(radius: 3)
                        .padding()
                    
                    VStack (alignment: .leading, spacing: 5){
                        
                        Text(conversation.recipient.name)
                            .font(Theme.headerFont)
                        HStack {
                            Image(systemName: "bubble.left.and.text.bubble.right.fill")
                                .font(.caption2)
                            Text(conversation.messages.last?.content ?? "No Messages")
                                .font(Theme.captionFont)
                        }
                        .foregroundStyle(.secondary)
                    }
                    .frame(alignment: .topLeading)
                    .padding()
                }
            
            }
            .frame(maxWidth:.infinity)
            .background{
                
                CardBackground(borderColor: Theme.defaultBorderColor, innerColor: Theme.defaultInnerColor)
                
            }
        }
    }
    
    public var body: some View {
        
        HStack{
            BackButton()
                .padding(.horizontal)
            Text("My Matches")
                .font(Theme.titleFont)
            Spacer()
        }
        List(conversations){conversation in
            conversationRow(conversation: conversation)
        }
        .scrollContentBackground(.hidden)
        .navigationBarHidden(true)
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
