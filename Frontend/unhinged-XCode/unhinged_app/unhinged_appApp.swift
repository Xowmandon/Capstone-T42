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
    
    enum AppRoute: Hashable {
        case login
        case buildProfile
        case match
    }
    
    @StateObject    var appModel            : AppModel              = AppModel()
    @StateObject    var serverPoll          : ServerPollingRepeater = ServerPollingRepeater()
    @State          var userIsAuthenticated : Bool                  = false
    //@State          var navPath             : [AppRoute]            = [.login]
    
    //TODO: get token from keychain and do auth check
    private var account : AccountData = AccountData.shared
    private var isFirstLogin : Bool = true
    //@State private var userIsAuthenticated : Bool = false
    
    init(){
        let defaults = UserDefaults.standard
        userIsAuthenticated = defaults.bool(forKey: "UserIsAuthenticated")
        print("Initial Authentication State:\(String(describing: userIsAuthenticated))")
        
        self.isFirstLogin = account.isFirstLogin
        print("Is first login: \(isFirstLogin)")
    }
    var body: some Scene {
        // LoginView(isFirstLogin: account.isFirstLogin, userIsAuthenticated: $userIsAuthenticated)
        /*
         BuildProfileView(isFirstTimeCreation: isFirstLogin, profile: Profile(name: account.fullName))
             .onAppear {
                 account.finishedFirstTimeSetup()
             }
         */
        WindowGroup {
            NavigationStack {
                if userIsAuthenticated {
                    if isFirstLogin {
                        BuildProfileView(isFirstTimeCreation: isFirstLogin, profile: Profile(name: account.fullName))
                            .onAppear {
                                account.finishedFirstTimeSetup()
                            }
                    } else {
                        
                        MatchView()
                        
                    }
                } else {
                    LoginView(isFirstLogin: account.isFirstLogin, userIsAuthenticated: $userIsAuthenticated)
                }
            }
            .environmentObject(appModel)
        }
        
    }
}
