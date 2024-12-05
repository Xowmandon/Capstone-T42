//
//  unhinged_appApp.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import SwiftUI
import SwiftData
import AuthenticationServices

@main
struct unhinged_appApp: App {
    
    //TODO: @EnvironmentObject appModel : AppModel
    
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Item.self,
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()
    
    // TODO: Store user ID from ASAuthorization
    // TODO: Make LoginView the root View and configure
    
    func getAuthenticationStatus() {
        let appleIDProvider = ASAuthorizationAppleIDProvider()
        //appleIDProvider.getCredentialState(forUserID: appModel.account.userID?, completion: <#T##(ASAuthorizationAppleIDProvider.CredentialState, (any Error)?) -> Void#>)
    }
    
    var body: some Scene {
        
        WindowGroup {
            NavigationStack{
                MatchView()
                    .navigationTitle("Find a Match")
            }
        }
        .modelContainer(sharedModelContainer)
    }
}
