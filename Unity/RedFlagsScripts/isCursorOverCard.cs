using UnityEngine;

[RequireComponent(typeof(Collider2D))]
public class isCursorOverCard : MonoBehaviour
{
    [Header("Scale settings")]
    [SerializeField] private float CardScaleFactor = 1.5f;

    [Header("Shadow settings")]
    [SerializeField] private Transform shadowTransform;
    [SerializeField] private Vector2 shadowOffset = new(0.2f, -0.2f);

    private Vector3 TargetShadowPos;
    private Vector3 scalefactor;
    private Vector3 depthOffset = new(0f, 0f, 0.1f);

    private bool isCursorOver = false;

    void OnMouseEnter()
    {
        isCursorOver = true;
        transform.GetChild(0).position = transform.GetChild(0).position -depthOffset;
    }

    private void Update()
    {
        if(isCursorOver)
        {
            if(transform.localScale.x != CardScaleFactor)
            {
                CardScale();
                OffsetShadow();
            }
        }
        else
        {
            if(transform.localScale.x != 1f)
            {
                if(Input.GetMouseButton(0)) return;
                transform.localScale = Vector3.Lerp(transform.localScale, new(1f, 1f, 1f), Time.deltaTime * 50f);
                HideShadow();
            }
            if(transform.GetChild(0).localRotation.z != 0f)
            transform.GetChild(0).rotation = Quaternion.Lerp(transform.GetChild(0).rotation, Quaternion.identity, Time.deltaTime * 50f);
        }
    }

    void OnMouseExit()
    {
        isCursorOver = false;
        transform.GetChild(0).position = transform.GetChild(0).position +depthOffset;
    }

    private void CardScale()
    {
        scalefactor = new(CardScaleFactor, CardScaleFactor, 1f);
        transform.localScale = Vector3.Lerp(transform.localScale, scalefactor, Time.deltaTime * 50f);
    }

    private void OffsetShadow()
    {
        TargetShadowPos = new(transform.GetChild(0).position.x + shadowOffset.x, 
            transform.GetChild(0).position.y + shadowOffset.y, transform.GetChild(0).position.z + 0.1f);
        shadowTransform.position = Vector3.Lerp(shadowTransform.position, TargetShadowPos, Time.deltaTime * 50f);
    }

    private void HideShadow()
    {
        Vector3 targetPos = new(transform.GetChild(0).position.x, 
            transform.GetChild(0).position.y, transform.GetChild(0).position.z + 0.2f);
        shadowTransform.position = Vector3.Lerp(shadowTransform.position, targetPos, Time.deltaTime * 50f);
    }
}