//Author: Benjamin Steinberg
//Date Created: 12/11/2024
//Notes:

using UnityEngine;

public enum moveType
{
    Melee,
    Magic,
    Heal
}

public class attack : MonoBehaviour
{
    //public
    public moveType moveType;
    
    //private
    private RPGManager gamemanager;

    public void action()
    {
        gamemanager.receiveAction(moveType);
        Debug.Log("button pressed");
    }

    public void setGameManager(RPGManager gm)
    {
        gamemanager = gm;
    }
}