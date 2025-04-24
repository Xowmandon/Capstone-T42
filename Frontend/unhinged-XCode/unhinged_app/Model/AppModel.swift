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
    
    private var poller : ServerPollingRepeater?
    
    init() {
        
        self.prospectiveMatches = []
        self.conversations = []
        self.profile = Profile(name: AccountData.shared.fullName)
        self.startPolling()
        
    }
    
    func startPolling() {
        poller = ServerPollingRepeater()
        self.poller?.start()
    }
    func stopPolling(){
        self.poller?.stop()
    }
    
    func getClientUserProfile() async {
        let profile = await APIClient.shared.getProfile(userID: nil)
        self.profile = profile!
        return
    }
    
    func getSwipeProfiles() async {
        //API call returns profile data
        let pulledSwipeProfiles = await APIClient.shared.getSwipes(limit: 5)
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
            return
        }
        self.conversations = pulledConversations
    }
    
}
