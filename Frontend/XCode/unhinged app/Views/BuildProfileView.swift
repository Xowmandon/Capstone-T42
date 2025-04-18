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
    case attribute
}

struct BuildProfileView: View {
    
    //TODO: confirm changes upon dismiss
    //TODO: extract subviews
    let isFirstTimeCreation : Bool
    @State var hasMadeChanges : Bool = true
    
    @EnvironmentObject var appModel : AppModel
    @FocusState private var focusedField : BuildProfileFocusedField?
    var editButtonImage : String = "pencil.circle.fill"
    
    @State var profile : Profile
    var theme : Theme = Theme.shared
    
    @State var showAddObjectSheet : Bool = false
    @State var showAvatarBuilderSheet : Bool = false // TODO: Avatar Builder
    @State var attributes : [Attribute] = []
    @State var biographyText : String = ""
    
    public var body: some View {
        NavigationStack {
            ZStack {
            // Profile Content
                ScrollView {
                    Text("My Profile")
                        .font(Theme.titleFont)
                    
                    //Avatar Customization
                    VStack (alignment: .leading) {
                        Text("Avatar")
                            .font(Theme.headerFont)
                        HStack {
                            Circle()
                                .foregroundStyle(Color.blue)
                                .frame(maxWidth: 100)
                                .overlay{
                                    Image(systemName: "pencil.circle.fill")
                                        .font(.system(.title))
                                        .frame(minWidth: 100, minHeight: 100, alignment: .topTrailing)
                                }
                            VStack{
                                Text("<Select Head>")
                                Text("<Select Top>")
                                Text("<Select Bottom>")
                            }
                        }
                    }
                    ProfileCard(profileImage: $profile.image, name: $profile.name, age: $profile.age, isEditable: true, focusedField: $focusedField)
                        .frame(minHeight: 400)
                    // Basic Info (Attributes)
                    VStack (spacing : 10){
                        /*
                        HStack{
                            Text("Attributes")
                                .font(Theme.headerFont)
                                .padding()
                            Spacer()
                            //Edit Attributes Button
                            Button(action: {
                                profile.attributes.append(Attribute(customName: "ABC", symbolName: "house.fill"))
                                print("added attribute to profile")
                            }, label: {
                                Image(systemName: "plus.circle.fill").padding(.horizontal).font(.title2)
                            })
                        }
                        .padding(.top)
                        .padding(.horizontal)
                         */
                        //Location
                        VStack {
                            HStack {
                                Image(systemName: "mappin")
                                    .foregroundStyle(.secondary)
                                Text("Location:")
                                    .font(Theme.headerFont)
                                Spacer()
                            }
                            VStack (alignment: .leading){
                                HStack {
                                    Text("City:")
                                    TextField("City", text: $profile.city)
                                        .focused($focusedField, equals: .attribute)
                                        .background(Color(.quaternarySystemFill))
                                }
                                HStack{
                                    Text("State:")
                                    Picker("Select a State", selection: $profile.state) {
                                        ForEach(USState.allCases) { state in
                                            Text(state.fullName) // Display the full name of the state
                                                .tag(state) // Tag each picker item with the corresponding state
                                        }
                                    }
                                }
                            }
                            .padding(.leading)
                        }
                        .padding()
                        /*
                        ForEach($profile.attributes){ $attribute in
                            VStack (alignment: .leading){
                                Text("Custom Attribute")
                                HStack{
                                    //SF Symbol Picker
                                    Image(systemName: "pencil")
                                        .foregroundStyle(.secondary)
                                    TextField("Name", text: $attribute.customName)
                                        .focused($focusedField, equals: .attributeField)
                                        .background(Color(.quaternarySystemFill))
                                }
                            }
                            .padding()
                        }
                        Spacer()
                         */
                    }
                    .font(Theme.bodyFont)
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    }
                    
                    // Biography
                    VStack{
                        HStack{
                            Image(systemName: "star.fill")
                                .foregroundStyle(.secondary)
                            Text("About Me!")
                                .font(Theme.headerFont)
                            Spacer()
                            Button(action: {
                                focusedField = .biography
                            }, label: {
                                Image(systemName: editButtonImage).padding(.horizontal).font(.title2)
                            })
                            
                        }
                        .padding()
                        
                        TextEditor(text: $biographyText)
                            .focused($focusedField, equals: .biography)
                            .font(Theme.bodyFont)
                            .padding(.horizontal)
                            .padding(.bottom)
                            .onAppear(perform: {biographyText = profile.biography})
                            .frame(minHeight: 150)
                            
                    }
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                        
                    }
                    
                    
                    //TODO: Image Gallery
                    //Prompts
                    ForEach(profile.prompts){prompt in
                        ZStack (alignment:.topTrailing){
                            PromptView(prompt: prompt)
                            Button{
                              
                                //TODO: remove prompt from profile
                                
                            } label: {
                                Image(systemName: "trash.fill")
                                    .foregroundStyle(.red)
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                                    .padding()
                            }
                        }
                    }
                    Spacer()
                        .padding(.vertical, 60)
                }
                .padding()
                
                //UI Overlay
                VStack {
                    HStack{
                        if !isFirstTimeCreation {
                            BackButton()
                            Spacer()
                            Button {
                                saveProfile()
                                hasMadeChanges = false
                            } label: {
                                Image(systemName: "checkmark")
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                            }
                        } else {
                            Spacer()
                            NavigationLink(destination: MatchView().navigationBarBackButtonHidden(), label: {
                                Image(systemName: "checkmark")
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                            })
                        }
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
                        Button() {
                            focusedField = nil // Dismiss keyboard
                        } label: {
                            Image(systemName: "checkmark.circle.fill")
                        }
                    }
                    .fixedSize()
                }
            }
            //Add Object Sheet
            .sheet(isPresented: $showAddObjectSheet){
                AddObjectSheet(profile: $profile)
            }
        }
        .onDisappear(perform: saveProfile)
    }
    
    func saveProfile() {
        self.profile.biography = biographyText
        appModel.profile = self.profile
        //TODO: Push new profile data to server
        APIClient.shared.initProfile(profile: appModel.profile)
        
    }
}


struct AddObjectSheet : View {
    
    @Binding var profile : Profile
    
    var body: some View {
        NavigationStack{
            HStack(spacing: 10){
                BackButton()
                Text("Customize My Profile")
                    .font(Theme.titleFont)
            }
            .padding()
            List {
                Section {
                    VStack {
                        HStack {
                            Text("Add A Prompt")
                                .font(Theme.headerFont)
                                .padding()
                            Spacer()
                            
                            Image(systemName: "plus")
                                .imageScale(.large)
                                .symbolRenderingMode(.hierarchical)
                                .padding()
                                .background{
                                    CardBackground()
                                }
                                .padding()
                        }
                        Text("Keep your matches guessing with a custom prompt - be creative!")
                            .font(Theme.bodyFont)
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                    VStack {
                        PromptView(prompt: PromptItem.examplePrompt)
                            .padding(.horizontal)
                    
                    }
                    
                }
                
                Section{
                    VStack{
                        HStack {
                            Text("Add A Photo")
                                .padding()
                                .font(Theme.headerFont)
                            Spacer()
                            Image(systemName: "plus")
                                .imageScale(.large)
                                .symbolRenderingMode(.hierarchical)
                                .padding()
                                .background{
                                    CardBackground()
                                }
                                .padding()
                        }
                        Text("Decorate your profile with a photo.")
                    }
                    ImageGalleryCard()
                        .padding()
                }
            }
        }
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
    
    BuildProfileView(isFirstTimeCreation: false,profile: Profile())
        .environmentObject(AppModel())
    
}
