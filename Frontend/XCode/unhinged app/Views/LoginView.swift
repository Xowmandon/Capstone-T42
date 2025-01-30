//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI
import AuthenticationServices

struct LoginView: View {
    
    @Binding var userIsAuthenticated : Bool
    
    var body: some View {
        VStack {
            Spacer()
            Text("Welcome to")
            Text("UnHinged")
                .font(.system(.largeTitle, weight: .heavy))
            Spacer()
            
            if (!userIsAuthenticated) {
                SignInWithAppleButton(.signIn, onRequest: {requests in
                    requests.requestedScopes = [.email, .fullName]
                    let authController = ASAuthorizationController(authorizationRequests: [requests])
                    //authController.performRequests()
                }, onCompletion: { result in
                    
                    switch result {
                        
                    case .success(let auth):
                        print("authentication successful")
                        print(auth)
                        
                        guard let credentials = auth.credential as? ASAuthorizationAppleIDCredential else {return}
                        
                        let credentialEmail = credentials.email
                        let credentialFirstName = credentials.fullName?.givenName
                        let credentialLastName = credentials.fullName?.familyName
                        
                        print(credentials)
                        //guard let identityToken = credentials.identityToken, let identityTokenString = String(data: identityToken, encoding: .utf8) else { return }
                        //let body = ["appleIdentityToken": identityTokenString]
                        //guard let jsonData = try? JSONEncoder().encode(body) else { return }
                        // This is where you'd fire an API request to your server to authenticate with the identity token attached in the request headers.
                        
                        // Set account information
                        AccountData.shared.setEmail(credentialEmail!)
                        let accountProfile = Profile(name: (credentialFirstName ?? "nil"), imageName: "stockPhoto")
                        AccountData.shared.setProfile(accountProfile)
                        
                        
                        //Ensure account exists in DB
                        let accountExists : Bool = APIClient.shared.assertAccountExistence(userEmailID: credentialEmail!)
                        if (accountExists) {
                            
                        // Mark account's authentication status
                        AccountData.shared.authenticate()
                            
                            
                        } else {
                            
                            APIClient.shared.createAccount(account: AccountData.shared)
                            
                        }
                        
                        break
                        
                    case .failure(let error):
                        print(error)
                        break
                        
                    }
                    
                    
                    //Confirm authentication and go to match view
                    userIsAuthenticated = true
                    
                })
                .frame(width: 200, height: 60)
                .mask(RoundedRectangle(cornerRadius: 10, style: .continuous))
            } else {
                
                
            }
            
            /*
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .fill(.blue)
                .frame(width: 200, height: 60)
                .clipped()
                .overlay {
                    HStack {
                        Text("Sign in with Email")
                            .foregroundStyle(.white)
                        Image(systemName: "paperplane")
                            .font(.body)
                            .foregroundStyle(.white)
                    }
                }
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .fill(.blue)
                .frame(width: 200, height: 60)
                .clipped()
                .overlay {
                    HStack {
                        Text("Sign in with Google")
                            .foregroundStyle(.white)
                        Image(systemName: "paperplane")
                            .font(.body)
                            .foregroundStyle(.white)
                    }
                }
             */
            Spacer()
        }
        .frame(maxWidth: .infinity)
        .clipped()
        .padding(.top, 53)
        .padding(.bottom, 0)
        
    }
}

