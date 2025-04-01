//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI
import AuthenticationServices

struct LoginView: View {
    
    //TODO: move account information to appModel
    @Binding var userIsAuthenticated : Bool
    @State private var showErrorAlert = false
    @State private var errorMessage : String = ""
    
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
                .accessibilityIdentifier("Sign in with Apple")
            } else {
                Button(action: {
                    userIsAuthenticated.toggle()
                }) {
                    Text("Start Matching!")
                }
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
        .alert(isPresented: $showErrorAlert) {
            // Define the alert
            Alert(
                title: Text("Authentication Error"),
                message: Text(errorMessage),
                primaryButton: .default(Text("OK")),
                secondaryButton: .cancel()
            )
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
            print(userIdentifier, credentialEmail, credentialFirstName, credentialLastName, identityToken as Any, authorizationCode as Any)
            
            // Set account information
            AccountData.shared.setUserID(userIdentifier)
            AccountData.shared.setEmail(credentialEmail)
            let accountProfile = Profile(name: "\(credentialFirstName) \(credentialLastName)")
            AccountData.shared.setProfile(accountProfile)
            print("Set Account information:")
            print(AccountData.shared.getUserID() as Any, AccountData.shared.getEmail() as Any, AccountData.shared.getProfile().name)
            
            //Send identity token to backend server
            let identityTokenString = String(data: identityToken!, encoding: .utf8)
            ///print("Identity Token String: \(String(describing: identityTokenString))")
            APIClient.shared.sendIdentityToken(token: identityTokenString!) //Saves JWTToken to keychain
            
            //Ensure account exists in DB
            let accountExists : Bool = APIClient.shared.assertAccountExistence(userEmailID: credentialEmail)
            if (accountExists) {
                // Mark account's authentication status
                AccountData.shared.authenticate()
            } else {
                //APIClient.shared.createAccount(account: AccountData.shared)
            }
            
            //Save basic profile information to DB
            
            //Assert Apple Credential State
            
            let provider = ASAuthorizationAppleIDProvider()
            
            provider.getCredentialState(forUserID: userIdentifier){
                credentialState, error in
                
                switch credentialState {
                case .authorized:
                    print("Credential state is authorized")
                case .revoked:
                    print("Credential state is revoked")
                case .notFound:
                    print("Credential state is not found")
                case .transferred:
                    print("Credential state transferred")
                @unknown default:
                    fatalError()
                }
            }
            
            //Present Main View
            userIsAuthenticated = true
            
            //TODO: present profile creation view upon first account creation
            
            break
        case .failure(let error):
            print("Authentication unsuccessful")
            errorMessage = "Authentication Error: \(error)"
            showErrorAlert = true
            break
        }
    }
}

#Preview {
    LoginView(userIsAuthenticated: .constant(false))
}
