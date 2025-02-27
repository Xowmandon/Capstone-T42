//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI
import AuthenticationServices

struct LoginView: View {
    
    @State private var showErrorAlert = false
    @Binding var userIsAuthenticated : Bool
    
    var body: some View {
        VStack {
            Spacer()
            Text("Welcome to")
                .font(Font.custom("PixelifySans-Regular", size: 18))
            HStack (spacing: 1){
                Text("Un")
                    .font(Font.custom("PixelifySans-Bold", size: 60))
                    .foregroundStyle(.purple)
                Text("hinged!")
                    .font(Font.custom("PixelifySans-Bold", size: 60))
            }
            Spacer()
            if (!userIsAuthenticated) {
                SignInWithAppleButton(.signIn, onRequest: {requests in
                    requests.requestedScopes = [.email, .fullName]
                }, onCompletion: {result in
                    handleAppleSignIn(result: result)
                })
                .frame(width: 200, height: 60)
                .mask(RoundedRectangle(cornerRadius: 10, style: .continuous))
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
    
    private func handleAppleSignIn(result: Result<ASAuthorization, Error>) {
        switch result {
        case .success(let auth):
            print("authentication successful")
            print(auth)
        
            guard let credentials = auth.credential as? ASAuthorizationAppleIDCredential else {
                print("Failed to get Apple ID credentials")
                return
            }

            let userIdentifier = credentials.user // Unique identifier for the user
            let credentialEmail = credentials.email ?? "No email provided" // User's email
            let credentialFirstName = credentials.fullName?.givenName ?? "No first name" // User's first name
            let credentialLastName = credentials.fullName?.familyName ?? "No last name" // User's last name
            let identityToken = credentials.identityToken // JWT for backend verification
            let authorizationCode = credentials.authorizationCode // Short-lived token for backend use
        
            print("Got Credentials:")
            print(credentialEmail, credentialFirstName, credentialLastName, identityToken, authorizationCode)
            
            // Set account information
            AccountData.shared.setEmail(credentialEmail)
            let accountProfile = Profile(name: "\(credentialFirstName) \(credentialLastName)", imageName: "stockPhoto")
            AccountData.shared.setProfile(accountProfile)
            print("Set Account information:")
            print(AccountData.shared.getUserID(), AccountData.shared.getEmail(), AccountData.shared.getProfile().name)
            
            //Send identity token to backend server
            let identityTokenString = String(data: identityToken!, encoding: .utf8)
            print("Identity Token String: \(identityTokenString)")
            APIClient.shared.sendIdentityToken(token: identityTokenString!)
            
            //Ensure account exists in DB
            let accountExists : Bool = APIClient.shared.assertAccountExistence(userEmailID: credentialEmail)
            if (accountExists) {
                // Mark account's authentication status
                AccountData.shared.authenticate()
            } else {
                //APIClient.shared.createAccount(account: AccountData.shared)
            }
            //Present Main View
            userIsAuthenticated = true
            break
        case .failure(let error):
                print("Authentication unsuccessful")
                print(error)
                showErrorAlert = true
                break
        }
    }
}

/*
 import SwiftUI
 import AuthenticationServices

 struct LoginView: View {
     @State private var userIsAuthenticated = false
     @State private var showErrorAlert = false
     @State private var errorMessage = ""

     var body: some View {
         VStack {
             if !userIsAuthenticated {
                 SignInWithAppleButton(.signIn, onRequest: { request in
                     request.requestedScopes = [.email, .fullName]
                 }, onCompletion: handleAppleSignIn)
                 .frame(width: 200, height: 60)
                 .mask(RoundedRectangle(cornerRadius: 10, style: .continuous))
             } else {
                 Text("Welcome!")
             }
         }
         .alert(isPresented: $showErrorAlert) {
             Alert(title: Text("Error"), message: Text(errorMessage), dismissButton: .default(Text("OK")))
         }
     }

     private func handleAppleSignIn(result: Result<ASAuthorization, Error>) {
         switch result {
         case .success(let auth):
             guard let credentials = auth.credential as? ASAuthorizationAppleIDCredential else { return }
             guard let credentialEmail = credentials.email else {
                 print("Email is nil")
                 return
             }

             let credentialFirstName = credentials.fullName?.givenName
             let credentialLastName = credentials.fullName?.familyName

             AccountData.shared.setEmail(credentialEmail)
             let accountProfile = Profile(name: (credentialFirstName ?? "nil"), imageName: "stockPhoto")
             AccountData.shared.setProfile(accountProfile)

             APIClient.shared.assertAccountExistence(userEmailID: credentialEmail) { accountExists in
                 DispatchQueue.main.async {
                     if accountExists {
                         AccountData.shared.authenticate()
                     } else {
                         APIClient.shared.createAccount(account: AccountData.shared) { success in
                             if success {
                                 AccountData.shared.authenticate()
                             }
                         }
                     }
                     userIsAuthenticated = true
                 }
             }

         case .failure(let error):
             print("Authentication failed: \(error.localizedDescription)")
             DispatchQueue.main.async {
                 self.showErrorAlert = true
                 self.errorMessage = error.localizedDescription
             }
         }
     }
 }
 
 
 */

#Preview {
    
    LoginView(userIsAuthenticated: .constant(false))
    
}
