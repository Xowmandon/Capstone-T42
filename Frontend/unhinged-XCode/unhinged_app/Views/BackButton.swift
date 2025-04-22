//
//  BackButton.swift
//  unhinged app
//
//  Created by Harry Sho on 11/26/24.
//

import SwiftUI

struct BackButton : View {
    
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Button(action: { dismiss() }) {
            Image(systemName: "chevron.left")
                .padding()
                .background{
                    CardBackground(borderColor: Theme.defaultBorderColor, innerColor: Theme.defaultInnerColor)
                }
        }
    }
    
}

#Preview {
    VStack {
        BackButton()
    }
}
