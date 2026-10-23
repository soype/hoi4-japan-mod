# Strike the Southern Road - Axis Negotiations

A small Hearts of Iron IV mod that expands `JAP_strike_the_southern_road` for
games where the Axis has already conquered the Western colonial empires.

If a Tripartite Pact partner (Germany, Italy, an Axis member, or one of their
puppets) controls any of the Southern Resource Area states, Japan first opens
negotiations instead of immediately gaining wargoals. The partner can honor the
pact, demand compensation, or refuse. Refusal breaks the pact and gives Japan
the wargoals.

## Build

The mod overrides only one focus, but HOI4 requires the whole
`common/national_focus/japan.txt` file to be overridden. The generated file is
not tracked in git. Rebuild it from the installed game files with:

```bash
python3 tools/build_focus.py
```

If the game is installed somewhere unusual:

```bash
python3 tools/build_focus.py "/path/to/Hearts of Iron IV/common/national_focus/japan.txt"
```

The tracked source for the focus is
`src/focus/JAP_strike_the_southern_road.txt`. Edit that file, not the generated
`common/national_focus/japan.txt`.

## Files

- `common/scripted_triggers/JAP_southern_road_triggers.txt` - target states,
  Tripartite signatory checks, region checks, and Japan's AI condition.
- `common/scripted_effects/JAP_southern_road_effects.txt` - cession,
  compensation, pact break, and wargoal effects.
- `events/JAP_southern_road.txt` - the six-event negotiation chain.
- `localisation/english/JAP_southern_road_l_english.yml` - all text.
- `src/focus/JAP_strike_the_southern_road.txt` - modified focus definition.
- `tools/build_focus.py` - generates the full focus-tree override.

## Event chain

| Event | Recipient | Meaning |
|---|---|---|
| `JAP_southern_road.1` | Tripartite partner | Japan requests the territories. |
| `JAP_southern_road.2` | Japan | The partner cedes the territories. |
| `JAP_southern_road.3` | Japan | The partner demands payment. |
| `JAP_southern_road.4` | Japan | The partner breaks the pact; wargoals granted. |
| `JAP_southern_road.5` | Tripartite partner | Japan accepts the terms; cession + compensation. |
| `JAP_southern_road.6` | Tripartite partner | Japan rejects the terms; triggers `.4`. |

## Compensation

If the partner ceded the Dutch East Indies, they receive resource rights in
West Java (state 335) and offsite industry matching Batavia (state 1058):
1 civilian and 2 military factories.

If they ceded Malaya, they receive the tungsten of Pahang (state 1063). The
`resources = { tungsten }` filter is used; if the game grants all resources in
the state instead, that is the intended fallback.

Indochina and the Philippines use their ceded states for resource rights as a
fallback, since the original request did not specify separate terms for them.

## Notes

- The Tripartite Pact in vanilla is not a faction. It is represented by
  guarantees and non-aggression pacts. The signatory check therefore treats
  `JAP_sea_tripartite_pact` plus GER/ITA/Axis membership and their subjects as
  the pact bloc.
- The request text used state 1035 for Batavia, but the vanilla state ID is
  **1058** (state 1035 is Nanjing). The mod uses 1058.
- The request text used "province 1063"; 1063 is a **state** ID (Pahang).
- Historical AI Japan refuses to pay unless the Axis is at war with the USSR
  and the USSR is losing (`surrender_progress > 0.5`) or the Axis is clearly
  stronger (`strength_ratio > 1.5`). This matches the requested "sign of
  weakness" logic.
- Breaking the pact cancels the non-aggression pact, applies the vanilla
  `refused_tripartite_pact_opinion` modifier in both directions, and removes
  Japan from the partner's faction if they somehow share one.
- If a partner holds only part of a region, the whole vanilla wargoal branch
  for that region is skipped. The negotiation covers the partner's holdings,
  but Japan does not automatically gain wargoals on the rest of that region.
- The mod overrides `common/national_focus/japan.txt`, so it will conflict with
  other mods that also override Japan's focus tree.

## Testing

1. Enable the mod in the launcher.
2. Start as Japan, use `focus.autocomplete` and `focus.nochecks` if needed.
3. Tag-switch to Germany, conquer the Netherlands/France/Britain, and puppet
   or annex the colonies.
4. Complete `JAP_strike_the_southern_road` and verify the event chain.
5. Check `logs/error.log` for script errors after each run.
