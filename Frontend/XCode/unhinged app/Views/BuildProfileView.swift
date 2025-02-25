//
//  BuildProfileView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI

struct BuildProfileView: View {
    
    var profile : Profile = AccountData.shared.getProfile()
    var theme : Theme = Theme.shared
    
    @State private var showAddObjectSheet : Bool = false
    
    public var body: some View {
        ZStack {
            
            // Profile Content
            ScrollView{
                
                
                Text("My Profile")
                    .font(Theme.titleFont)
                
                //Avatar Customization
                Text("Avatar")
                    .font(Theme.headerFont)
                    
                Circle()
                    .foregroundStyle(Color.blue)
                    .frame(maxWidth: 100)
                    .overlay{
                        Image(systemName: "pencil.circle.fill")
                            .font(.system(.title))
                            .frame(minWidth: 100, minHeight: 100, alignment: .topTrailing)
                    }
                
                
                ProfileCard(profile: profile)
                    .padding(.horizontal)
                    .frame(minHeight: 400)
                
                // Basic Info (Attributes?)
                
                VStack (spacing: 5){
                    
                    
                    ForEach(profile.attributes, id: \.self) { attribute in
                        
                        HStack{
                            
                            Image(systemName: attribute.symbolName)
                            Text(attribute.customName)
                                .font(Theme.bodyFont)
                            
                        }
                        
                    }
                    
                    
                }
                .padding()
                .frame(maxWidth:.infinity)
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                .padding()
                
                //About Me
                
                VStack{
                    
                    HStack{
                        
                        Text("About Me!")
                            .font(Theme.headerFont)
                            .padding(.top)
                            .padding(.horizontal)
                        Spacer()
                        
                    }
                    
                    Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Curabitur euismod, eros at tincidunt sollicitudin, justo neque suscipit nunc, id fringilla odio erat eget sapien. ")
                        .font(Theme.bodyFont)
                        .padding()
                    
                    
                }
                .padding()
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                .padding(.horizontal)
                
                //TODO: Image Gallery
                
                
                //Prompts
                
                ForEach(profile.prompts ?? []){prompt in
                    
                    PromptView(prompt: prompt)
                        .padding()
                    
                    
                }
                
                
            }
            
            //Overlay
            VStack {
                
                HStack{
                    
                    BackButton()
                    Spacer()
                    
                }
                
                Spacer()
                Button(action: {showAddObjectSheet.toggle()}){
                    Image(systemName: "plus")
                        .imageScale(.large)
                        .symbolRenderingMode(.monochrome)
                        .foregroundStyle(.green)
                        .font(.system(.title, weight: .black))
                        .padding()
                        .background{
                            
                            Circle()
                                .fill(.ultraThickMaterial)
                                .shadow(radius: 5)
                        }
                }
            }
        }
        .navigationBarBackButtonHidden()
        .sheet(isPresented: $showAddObjectSheet){
            
            VStack {
                Text("Customize Your Profile")
                    .font(.headline)
                    .padding()
                VStack {
                    HStack {
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                        Text("Add A Prompt")
                            .padding()
                            .font(.system(.title3, weight: .medium))
                        Spacer()
                    }
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(Color(.secondarySystemBackground))
                        .frame(maxWidth: .infinity, maxHeight: 200)
                        .clipped()
                        .padding(20)
                        .overlay {
                            VStack {
                                Text("What is my favorite food?")
                                    .font(.headline)
                                    .foregroundStyle(.primary)
                                RoundedRectangle(cornerRadius: 10, style: .continuous)
                                    .fill(.orange)
                                    .frame(width: 100, height: 40)
                                    .clipped()
                                    .overlay {
                                        Text("Carrot")
                                    }
                                RoundedRectangle(cornerRadius: 10, style: .continuous)
                                    .fill(.pink)
                                    .frame(width: 100, height: 40)
                                    .clipped()
                                    .overlay {
                                        Text("Cake")
                                    }
                            }
                        }
                }
                VStack {
                    HStack {
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                        Text("Add A Photo")
                            .padding()
                            .font(.system(.title3, weight: .medium))
                        Spacer()
                    }
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(Color(.secondarySystemBackground))
                        .frame(maxWidth: .infinity, maxHeight: 200)
                        .clipped()
                        .padding(20)
                        .overlay {
                            VStack {
                                HStack {
                                    Text("My Favorite Place")
                                        .font(.headline)
                                        .foregroundStyle(.primary)
                                        .padding(.horizontal, 40)
                                    Spacer()
                                }
                                Image("myImage")
                                    .renderingMode(.original)
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .frame(maxWidth: .infinity, maxHeight: 130)
                                    .clipped()
                                    .overlay {
                                        Group {
                                            
                                        }
                                    }
                                    .mask {
                                        RoundedRectangle(cornerRadius: 20, style: .continuous)
                                            .frame()
                                            .clipped()
                                    }
                            }
                        }
                }
            }
            
        }
    }
    
    func saveProfile() {
        
        AccountData.shared.setProfile(self.profile)
        
    }
}

#Preview{
    
    BuildProfileView()
    
}
