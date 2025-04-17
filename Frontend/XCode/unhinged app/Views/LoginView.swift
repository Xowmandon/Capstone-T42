//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI
import AuthenticationServices

struct LoginView: View {
    let isFirstLogin : Bool
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
        let defaults = UserDefaults.standard
        
        switch result {
        case .success(let auth):
            print("authentication successful")
            print(auth)
            guard let credentials = auth.credential as? ASAuthorizationAppleIDCredential else {
                print("Failed to get Apple ID credentials")
                return
            }
            let userIdentifier = credentials.user // Unique identifier for the user
            let credentialEmail = credentials.email ?? "None" // User's email
            let credentialFirstName = credentials.fullName?.givenName ?? "None" // User's first name
            let credentialLastName = credentials.fullName?.familyName ?? "None" // User's last name
            let identityToken = credentials.identityToken // JWT for backend verification
            let authorizationCode = credentials.authorizationCode // Short-lived token for backend use
            print("Got Credentials:")
            print(userIdentifier, credentialEmail, credentialFirstName, credentialLastName, identityToken as Any, authorizationCode as Any)
            
            //Assert Apple Credential State
            let provider = ASAuthorizationAppleIDProvider()
            provider.getCredentialState(forUserID: userIdentifier){
                credentialState, error in
                switch credentialState {
                case .authorized:
                    print("Credential state is authorized")
                    defaults.set(true, forKey: "UserIsAuthenticated")
                    break
                case .revoked:
                    print("Credential state is revoked")
                    authenticationFailed(error: error)
                    return
                case .notFound:
                    print("Credential state is not found")
                    authenticationFailed(error: error)
                    return
                case .transferred:
                    print("Credential state transferred")
                    authenticationFailed(error: error)
                    return
                @unknown default:
                    fatalError()
                }
            }
            
            //Send identity token to backend server and save JWT to keychain
            let identityTokenString = String(data: identityToken!, encoding: .utf8)
            ///print("Identity Token String: \(String(describing: identityTokenString))")
            APIClient.shared.sendIdentityToken(token: identityTokenString!)
            
            // Set account information
            if isFirstLogin {
                if let userID = defaults.string(forKey: "UserID"),
                   let email = defaults.string(forKey: "UserEmail"),
                   let firstName = defaults.string(forKey: "UserFirstName"),
                   let lastName = defaults.string(forKey: "UserLastName") {
                    print("Set Account information in User defaults:")
                    print(userID, email, firstName, lastName)
                }
            } else {
                print (AccountData.shared.fullName)
            }
            userIsAuthenticated = true
            //TODO: present profile creation view upon first account creation
            break
        case .failure(let error):
            authenticationFailed(error: error)
            break
        }
    }
    
    func authenticationFailed(error: (any Error)? = nil){
        
        print("Authentication unsuccessful")
        errorMessage = "Authentication Error: \(String(describing: error))"
        showErrorAlert = true
        userIsAuthenticated = false
        return
    }
    
}

#Preview {
    LoginView(isFirstLogin: true,userIsAuthenticated: .constant(false))
}
