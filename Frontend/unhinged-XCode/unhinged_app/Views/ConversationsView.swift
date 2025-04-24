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
    @State var loading = true
    
    @ViewBuilder
    func conversationRow(conversation: Conversation) -> some View {
        
        NavigationLink(destination: MessageView(profile: conversation.matchedProfile, matchId: conversation.matchId ?? "")){
            
            VStack(alignment: .leading){
                HStack{
                    conversation.matchedProfile.image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 70, height: 70)
                        .clipShape(Circle())
                        .shadow(radius: 3)
                        .padding()
                    
                    VStack (alignment: .leading, spacing: 5){
                        
                        Text(conversation.matchedName ?? "No name")
                            .font(Theme.headerFont)
                        HStack {
                            Image(systemName: "bubble.left.and.text.bubble.right.fill")
                                .font(.caption2)
                            Text(conversation.lastMessage ?? "No messages")
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
        
        if !loading {
            HStack{
                BackButton()
                    .padding(.horizontal)
                Text("My Matches")
                    .font(Theme.titleFont)
                Spacer()
            }
            if appModel.conversations.isEmpty {
                VStack{
                    Spacer()
                    Image(systemName: "heart.fill")
                        .foregroundColor(.gray)
                        .foregroundStyle(.tertiary)
                    Text("No Matches yet!")
                        .foregroundStyle(.secondary)
                    Spacer()
                }
            }
            List(appModel.conversations){conversation in
                conversationRow(conversation: conversation)
            }
            .scrollContentBackground(.hidden)
            .navigationBarHidden(true)
        } else {
            ProgressView("Loading...").foregroundStyle(.primary)
                .onAppear{
                    getConversations()
                }
            
        }
        
    }
    
    // Query database for conversations associated with client account
    private func getConversations() {
        Task {
            await appModel.getConversations()
            loading = false
        }
        return
    }
    
}


#Preview {
    NavigationStack{
        //ConversationsView()
    }
}
