//
//  AppModel.swift
//  unhinged app
//
//  Created by Harry Sho on 12/8/24.
//

import Foundation
import SwiftUI

@MainActor
final class AppModel : ObservableObject {
    
    @Published var profile : Profile
    @Published var matchPreferences : MatchPreference?
    
    @Published var prospectiveMatches : [Profile]
    @Published var conversations : [Conversation]
    
    init() {
        
        self.prospectiveMatches = []
        self.conversations = []
        self.profile = Profile(name: AccountData.shared.fullName)
        
    }
    
    func getClientUserProfile() async {
        Task {
            let profile = await APIClient.shared.getProfile(userID: nil)
            self.profile = profile!
        }
        return
    }
    
    func getSwipeProfiles() async {
        //API call returns profile data
        let pulledSwipeProfiles = await APIClient.shared.getSwipes(limit: 10)
        guard !pulledSwipeProfiles.isEmpty else {
            print("No profiles found.")
            return
        }
        self.prospectiveMatches.append(contentsOf: pulledSwipeProfiles)
    }
    
    func getConversations() async {
        let pulledConversations = await APIClient.shared.getMatches()
        guard !pulledConversations.isEmpty else {
            print("No conversations found.")
            self.conversations.append(Conversation(matchId: "", matchedUserId: "", matchedName: "", matchDate: "", lastMessage: "", id: UUID(), matchedProfile: Profile(name: "apple"), messages: [], hasUnreadMessages: false))
            return
        }
        self.conversations = pulledConversations
        self.conversations.append(Conversation(matchId: "", matchedUserId: "", matchedName: "", matchDate: "", lastMessage: "", id: UUID(), matchedProfile: Profile(name: "DEBUG"), messages: [], hasUnreadMessages: false))
    }
    
}
