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
    
    //TODO: get token from keychain and do auth check
    // TODO: Make LoginView the root View and add authentication check
    
    private var account : AccountData = AccountData.shared
    //@State private var userIsAuthenticated : Bool = false
    
    init(){
        
        //self.appModel.userIsAuthenticated = getAuthenticationStatus(account: self.account)
        self.account = AccountData(hasBeenAuthenticated: false, email: "")
        
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
                if appModel.userIsAuthenticated {
                    
                    MatchView()
                    
                } else {
                    
                    LoginView(userIsAuthenticated: $appModel.userIsAuthenticated)
                    
                }
            }
            .environmentObject(appModel)
        }
        
    }
}
