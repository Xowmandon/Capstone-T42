//
//  unhinged_appApp.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import SwiftUI
import AuthenticationServices

@main
struct unhinged_appApp: App {
    
    @StateObject var appModel : AppModel = AppModel()
    
    // TODO: Store user ID from ASAuthorization
    // TODO: Make LoginView the root View and add authentication check
    
    private var account : AccountData = AccountData.shared
    
    @State private var userIsAuthenticated : Bool = false
    
    init(){
        
        self.account = AccountData(hasBeenAuthenticated: false, email: "")
        
        userIsAuthenticated = getAuthenticationStatus(account: self.account)
        
        APIClient.shared.test_post_user()
        
    }
    
    func getAuthenticationStatus(account: AccountData) -> Bool {
        var success : Bool = false
        let appleIDProvider = ASAuthorizationAppleIDProvider()
        appleIDProvider.getCredentialState(forUserID: account.getUserID() ?? "0"){ credentialState, error in
            
            if (credentialState == .authorized){
                
                success = true
                
            }
            
        }
        
        return success
    }
    
    var body: some Scene {
        
        WindowGroup {
            NavigationStack{
                if userIsAuthenticated {
                    
                    MatchView()
                        .navigationTitle("Find a Match")
                    
                } else {
                    
                    LoginView(userIsAuthenticated: $userIsAuthenticated)
                    
                }
            }
            .environmentObject(appModel)
        }
        
    }
}
