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
        
    }
    
    func getAuthenticationStatus(account: AccountData) -> Bool {
        var success : Bool = false
        let appleIDProvider = ASAuthorizationAppleIDProvider()
        appleIDProvider.getCredentialState(forUserID: account.getUserID() ?? "0"){ credentialState, error in
            
            if (credentialState == .authorized){
                
                
                //Retrieve account information from backend
                
                
                
                //Login Successful, Present Match View to user
                success = true
                
            } else {
                
                //Login Denied
                success = false
            }
            
        }
        
        return success
    }
    
    var body: some Scene {
        
        WindowGroup {
            NavigationStack{
                if userIsAuthenticated {
                    
                    MatchView()
                    
                } else {
                    
                    LoginView(userIsAuthenticated: $userIsAuthenticated)
                    
                }
            }
            .environmentObject(appModel)
        }
        
    }
}
