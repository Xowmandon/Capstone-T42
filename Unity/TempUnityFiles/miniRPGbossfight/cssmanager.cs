//Author: Benjamin Steinberg
//Created by: 12/11/2024

using UnityEngine;
using UnityEngine.UI;

public class cssmanager : MonoBehaviour
{
    public roster choice;
    public Button[] buttonArr;

    void Awake()
    {
        for(int i = 0; i < buttonArr.Length; i++)
        {
            buttonArr[i].GetComponentInParent<cssButton>().setCSSManager(this);
        }
    }

    public void setChoice(roster selected)
    {
        choice = selected;
        Debug.Log(choice);
    }
}