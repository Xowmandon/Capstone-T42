//
//  SwiftUIView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI

struct LoginView: View {
    var body: some View {
        VStack {
            Spacer()
            Text("Welcome to")
            Text("UnHinged")
                .font(.system(.largeTitle, weight: .heavy))
            Spacer()
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
