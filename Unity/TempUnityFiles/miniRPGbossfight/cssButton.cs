//Author: Benjamin Steinberg
//Created by: 12/11/2024

using UnityEngine;

public class cssButton : MonoBehaviour
{
    public roster archetype;
    public cssmanager cssmanager;

    public void chooseCharacter()
    {
        cssmanager.setChoice(archetype);
    }

    public void setCSSManager(cssmanager manager)
    {
        cssmanager = manager;
    }
}
