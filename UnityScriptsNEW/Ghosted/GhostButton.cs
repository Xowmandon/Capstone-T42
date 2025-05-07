//Author: Allison Tang

using UnityEngine;
using UnityEngine.UI;

public class GhostButton : MonoBehaviour
{
    public string ghostID;
    private GhostGameManager gameManager;

    public void Init(string id, Sprite ghostSprite, GhostGameManager gm){
        ghostID = id;
        gameManager = gm;
        GetComponent<Image>().sprite = ghostSprite;
    }

    public void OnClick(){
        gameManager.CheckGhost(ghostID);
    }
}
