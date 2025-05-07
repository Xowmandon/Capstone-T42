//Author: Benjamin Steinberg
//Created: 12/11/2024

using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;
using System;

public enum StatusType { none, HeartBroken, Ghosted, Lovebombed }

public class rpgcharacter : MonoBehaviour
{
    public Image healthbar;
    public Image statusEffectIcon;
    public TMP_Text displayName;
    public Animator animator;
    public string charName;
    public bool madeMove = false;

    public virtual float MaxHealth => 70;
    protected virtual float MeleeAttackDam => 10;
    protected virtual float MagicAttackDam => 45;
    protected virtual float HealAmount => 40;
    protected virtual float UltimateDamage => 60;

    public float health;
    protected bool isDead = false;
    protected RPGManager gamemanager;
    public Dictionary<string, int> cooldowns = new();
    public StatusType currentStatus = StatusType.none;
    protected int statusDuration = 0;
    public StatusType getStatusEffect() => currentStatus;
    public int getStatusDuration() => statusDuration;

    protected virtual void Awake()
    {
        health = MaxHealth;
        animator = GetComponentInChildren<Animator>();
        updateHealthbar();
        cooldowns["Ultimate"] = 2;
        statusEffectIcon.enabled = false;
    }

    public bool getIsDead() => isDead;

    public void receiveDamage(float damage)
    {
        health -= damage;
        health = Mathf.Clamp(health, 0f, MaxHealth);
        updateHealthbar();

        if (health <= 0 && !isDead)
        {
            isDead = true;
            SpriteRenderer sr = GetComponentInChildren<SpriteRenderer>();
            if (sr != null)
            {
                sr.color = Color.gray;
            }
            died();
        }
    }

    public virtual void died()
    {
        gamemanager.deathDispatcher(this);
    }

    public void healHealth(float amount)
    {
        health = Mathf.Min(MaxHealth, health + amount);
        updateHealthbar();
    }

    public void meleeAttack(rpgcharacter enemy)
    {
        StartCoroutine(AttackRoutine(enemy, MeleeAttackDam, "Attack", Vector3.right * 0.5f));
    }

    public void magicAttack(rpgcharacter enemy)
    {
        StartCoroutine(AttackRoutine(enemy, MagicAttackDam, "Cast", Vector3.up * 0.4f));
    }

    public void ultimateAttack(rpgcharacter enemy)
    {
        if (cooldowns.ContainsKey("Ultimate"))
        {
            gamemanager.dialogueManager.EnqueueDialogue(new DialogueEntry($"{charName}'s Ultimate is still on cooldown!"));
            return;
        }
        cooldowns["Ultimate"] = 3;
        StartCoroutine(AttackRoutine(enemy, UltimateDamage, "Ultimate", Vector3.right * 0.8f));
    }

    public void healAlly(rpgcharacter ally)
    {
        if (cooldowns.ContainsKey("Heal"))
        {
            gamemanager.dialogueManager.EnqueueDialogue(new DialogueEntry($"{charName}'s Heal is on cooldown!"));
            return;
        }
        cooldowns["Heal"] = 2;
        ally.healHealth(HealAmount);
        animator?.SetTrigger("Heal");
    }

    public void updateHealthbar()
    {
        if (healthbar == null)
        {
            Debug.LogWarning($"{charName}'s healthbar is not assigned!");
            return;
        }
        healthbar.fillAmount = health / MaxHealth;
    }

    public void getGameMan(RPGManager gm) => gamemanager = gm;

    public void applyStatus(StatusType type, int duration)
    {
        if (currentStatus != StatusType.none || isDead || duration == 0) return; // Already afflicted, skip

        currentStatus = type;
        statusDuration = duration;

        if (statusEffectIcon == null || gamemanager == null || gamemanager.statusEffectSprites == null)
            return;

        int index = (int)type;
        if (index < 0 || index >= gamemanager.statusEffectSprites.Length) return;

        statusEffectIcon.sprite = gamemanager.statusEffectSprites[index];
        statusEffectIcon.enabled = true;
        statusEffectIcon.gameObject.SetActive(true);
    }


    public IEnumerator PreActionStatusCheckCoroutine(Action onBlocked)
    {
        if (currentStatus == StatusType.Ghosted)
        {
            gamemanager.dialogueManager.EnqueueDialogue(
                new DialogueEntry($"{charName} is Ghosted and too stunned to move!")
            );

            yield return new WaitUntil(() => gamemanager.dialogueManager.IsQueueEmpty());

            // Immediately run post-status logic after being blocked
            yield return gamemanager.StartCoroutine(PostActionStatusCheckCoroutine());

            onBlocked?.Invoke();
        }
    }


    public IEnumerator PostActionStatusCheckCoroutine()
    {
        if (currentStatus == StatusType.none)
            yield break;

        bool shouldClear = false;

        switch (currentStatus)
        {
            case StatusType.HeartBroken:
                receiveDamage(10);
                gamemanager.dialogueManager.EnqueueDialogue(
                    new DialogueEntry($"{charName} is HeartBroken and suffers from depression (damage)")
                );
                break;

            case StatusType.Lovebombed:
                if (statusDuration <= 0)
                {
                    receiveDamage(20);
                    gamemanager.dialogueManager.EnqueueDialogue(
                        new DialogueEntry($"{charName}'s Lovebomb exploded and caused damage!")
                    );
                    shouldClear = true;
                }
                break;

            case StatusType.Ghosted:
                // No damage, but we still want to check duration
                break;
        }

        yield return new WaitUntil(() => gamemanager.dialogueManager.IsQueueEmpty());

        statusDuration--;

        if (statusDuration < 0 || shouldClear)
        {
            string clearMessage = currentStatus switch
            {
                StatusType.Ghosted => $"{charName} is no longer Ghosted.",
                StatusType.HeartBroken => $"{charName} is no longer HeartBroken.",
                StatusType.Lovebombed => $"{charName} is no longer Lovebombed.",
                _ => $"{charName} is no longer afflicted."
            };

            gamemanager.dialogueManager.EnqueueDialogue(new DialogueEntry(clearMessage));
            yield return new WaitUntil(() => gamemanager.dialogueManager.IsQueueEmpty());

            currentStatus = StatusType.none;

            if (statusEffectIcon != null)
            {
                statusEffectIcon.enabled = false;
                statusEffectIcon.gameObject.SetActive(false);
            }
        }
    }

    public void reduceCooldowns()
    {
        List<string> keys = new List<string>(cooldowns.Keys);
        foreach (string key in keys)
        {
            cooldowns[key]--;
            if (cooldowns[key] <= 0)
                cooldowns.Remove(key);
        }
    }

    private IEnumerator AttackRoutine(rpgcharacter target, float damage, string animationTrigger, Vector3 moveDirection)
    {
        Vector3 startPos = transform.position;
        Vector3 movePos = startPos + moveDirection;

        animator?.SetTrigger(animationTrigger);

        float t = 0;
        while (t < 0.2f)
        {
            transform.position = Vector3.Lerp(startPos, movePos, t / 0.2f);
            t += Time.deltaTime;
            yield return null;
        }

        target.receiveDamage(damage);
        yield return new WaitForSeconds(0.3f);

        transform.position = startPos;
    }

    public void SetName(string name)
    {
        charName = name;

        if (displayName != null)
        {
            displayName.text = name;
            Debug.Log($"[SetName] Set display name to '{name}'");
        }
        else
        {
            Debug.LogWarning($"[SetName] displayName was null on {gameObject.name} when setting to '{name}'");
        }
    }
}
