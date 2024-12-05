//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI
import AuthenticationServices

struct LoginView: View {
    
    //@Environment(\.authorizationController) private var authorizationController
    
    //var
    
    var body: some View {
        VStack {
            Spacer()
            Text("Welcome to")
            Text("UnHinged")
                .font(.system(.largeTitle, weight: .heavy))
            Spacer()
            
            SignInWithAppleButton(.signIn, onRequest: {requests in
                
                requests.requestedScopes = [.email, .fullName]
                
            }, onCompletion: { result in
                
                switch result {
                    //TODO: API call for account information push
                case .success(let auth):
                    guard let credentials = auth.credential as? ASAuthorizationAppleIDCredential else {return}
                    let userID = credentials.user //pass to model
                    let email = credentials.email
                    //guard let identityToken = credentials.identityToken, let identityTokenString = String(data: identityToken, encoding: .utf8) else { return }
                    //let body = ["appleIdentityToken": identityTokenString]
                    //guard let jsonData = try? JSONEncoder().encode(body) else { return }
                    // This is where you'd fire an API request to your server to authenticate with the identity token attached in the request headers.
                    break
            
                case .failure(let error):
                    print(error)
                    break
                    
                }
                    
            })
            .frame(width: 200, height: 60)
            .mask(RoundedRectangle(cornerRadius: 10, style: .continuous))
            
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

#Preview {
    LoginView()
}
