//
//  BuildProfileView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI
import PhotosUI

enum BuildProfileFocusedField: Hashable {
    case none
    case name
    case biography
}

struct BuildProfileView: View {
    
    //TODO: confirm changes upon dismiss
    //TODO: use .overlay for edit button
    
    @State var profile : Profile
    var theme : Theme = Theme.shared
    var editButtonImage : String = "pencil.circle.fill"
    
    @State var showAddObjectSheet : Bool = false
    @State var showAvatarBuilderSheet : Bool = false // TODO: Avatar Builder
    //@State var showEditProfileCardSheet : Bool = false // TODO: Image Picker
    @State var showAttributeCreatorSheet : Bool = false  //TODO: Attribute builder
    
    @State var biographyText : String = ""
    
    /*
    
    @State var name : String
    @State var attributes : [Attribute]
    var prompts : [PromptItem]
    */
    
    @FocusState private var focusedField : BuildProfileFocusedField?
    /*
    init(){
        //Initialize variables with existing profile data
        _name = State(initialValue: (profile.name))
        _biography = State(initialValue: profile.biography ?? "No Bio written yet")
        _attributes = State(initialValue: profile.attributes)
        prompts = []
    }
     */
    public var body: some View {
        NavigationStack {
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
                    ProfileCard(profileImage: $profile.image, name: $profile.name, age: $profile.age, isEditable: true, focusedField: $focusedField)
                        .padding(.horizontal)
                        .frame(minHeight: 400)
                    
                    
                    // Basic Info (Attributes?)
                    ZStack(alignment:.topTrailing) {
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
                    }
                    
                    // Biography
                    VStack{
                        HStack{
                            Text("About Me!")
                                .font(Theme.headerFont)
                                .padding(.top)
                                .padding(.horizontal)
                            Spacer()
                            
                            Button(action: {
                                focusedField = .biography
                            }, label: {
                                Image(systemName: editButtonImage).padding(.horizontal).font(.title2)
                            })
                            
                        }
                        TextEditor(text:$biographyText)
                            .focused($focusedField, equals: .biography)
                            .font(Theme.bodyFont)
                            .padding()
                            .frame(minHeight: 10)
                            .onAppear{
                                biographyText = profile.biography ?? "Create a Biography..."
                            }
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
                    Spacer()
                        .padding(.vertical, 60)
                }
                
                //Overlay
                VStack {
                    HStack{
                        BackButton()
                        Spacer()
                    }
                    Spacer()
                    if focusedField == nil {
                        Button(action: {showAddObjectSheet.toggle()}){
                            Image(systemName: "plus")
                                .imageScale(.large)
                                .symbolRenderingMode(.monochrome)
                                .foregroundStyle(.green)
                                .font(.system(.title, weight: .black))
                                .padding()
                                .background{
                                    CardBackground()
                                }
                        }
                    }
                }
                .padding()
            }
            .navigationBarBackButtonHidden()
            .toolbar {
                ToolbarItem(placement: .keyboard) {
                    HStack{
                        Spacer()
                        Button("Done") {
                            focusedField = nil // Dismiss keyboard
                        }
                    }
                    .fixedSize()
                }
            }
            //Add Object Sheet
            .sheet(isPresented: $showAddObjectSheet){
                VStack {
                    Text("Customize Your Profile")
                        .font(Theme.headerFont)
                        .padding()
                    VStack {
                        HStack {
                            Text("Add A Prompt")
                                .font(Theme.headerFont)
                                .padding()
                            Spacer()
                            Image(systemName: "plus.app")
                                .imageScale(.large)
                                .symbolRenderingMode(.hierarchical)
                                .padding()
                        }
                        Text("Keep your matches guessing with a custom prompt - be creative!")
                            .font(Theme.bodyFont)
                            .padding()
                        PromptView(prompt: PromptItem.examplePrompt)
                            .padding()
                    }
                    VStack {
                        HStack {
                            Text("Add A Photo")
                                .padding()
                                .font(.system(.title3, weight: .medium))
                            Spacer()
                            Image(systemName: "plus.app")
                                .imageScale(.large)
                                .symbolRenderingMode(.hierarchical)
                                .padding()
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
                                                .clipped()
                                        }
                                }
                            }
                    }
                }
            }
        }
        
    }
    
    func saveProfile() {
        AccountData.shared.setProfile(self.profile)
        
        //TODO: Push new profile data to server
    }
}

private extension PhotosPickerItem {
    var identifier: String {
        guard let identifier = itemIdentifier else {
            fatalError("The photos picker lacks a photo library.")
        }
        return identifier
    }
}

#Preview{
    
    let profile = AccountData.shared.profile
    BuildProfileView(profile: profile)
    
}
