//
//  ProfileContentView.swift
//  
//
//  Created by Harry Sho on 4/25/25.
//


ScrollView {
                    if !isFirstTimeCreation {
                        Text("My Profile")
                            .font(Theme.titleFont)
                    } else {
                        Text("Create My Profile")
                            .font(Theme.titleFont)
                    }
                    /*
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
                    */
                    
                    ProfileCard(profileImage: $profile.image, name: $profile.name, age: $profile.age, isEditable: true, focusedField: $focusedField)
                        .frame(minHeight: 400)
                    
                    // MARK: Avatar Builder
                    
                    VStack {
                        Text("My Avatar")
                            .font(Theme.headerFont)
                        HStack {
                            AvatarPreview(avatar: avatar)
                                .frame(maxHeight: 200)
                            NavigationLink(destination: AvatarCreator(profileAvatar: $avatar).navigationBarBackButtonHidden()){
                                VStack {
                                    Image(systemName: "theatermask.and.paintbrush.fill")
                                    Text("Edit avatar")
                                }
                            }
                        }
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background{CardBackground()}
                    
                    // MARK: Basic Info (Attributes)
                    VStack (spacing : 10){

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
                        
                        TextEditor(text: $profile.biography)
                            .focused($focusedField, equals: .biography)
                            .font(Theme.bodyFont)
                            .padding(.horizontal)
                            .padding(.bottom)
                            //.onAppear(perform: {biographyText = profile.biography})
                            .frame(minHeight: 150)
                            
                    }
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                        
                    }
                    
                    
                    // MARK: Image gallery
                    
                    ForEach(galleryItems.indices, id: \.self) { index in
                        let photo = galleryItems[index]
                        ZStack(alignment: .topTrailing){
                            ImageGalleryCard(isEditable: false,
                                             galleryItem: $galleryItems[index],
                                             image: photo.image,
                                             title: photo.title,
                                             description: photo.description)
                            Button{
                                
                                galleryItemIDToDelete = galleryItems[index].id
                                deleteType = .gallery
                                isShowingDeleteConfirmation = true
                                                                 
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
                    
                    //Prompts
                    ForEach(prompts){ prompt in
                        ZStack (alignment:.topTrailing){
                            PromptView(prompt: prompt)
                            Button{
                                
                                promptItemIDToDelete = prompt.id
                                deleteType = .prompt
                                isShowingDeleteConfirmation = true
                                 
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