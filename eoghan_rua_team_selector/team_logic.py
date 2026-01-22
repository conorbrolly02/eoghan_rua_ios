
# team_logic.py
from typing import List, Tuple, Dict, Optional
import random

Skill = int
Player = Tuple[str, Skill]
WEIGHTS = {1: 3, 2: 2, 3: 1}


def _validate(players: List[Player], n_teams: int) -> None:
    if n_teams < 2:
        raise ValueError("Number of teams must be at least 2.")
    if len(players) < n_teams:
        raise ValueError("You have fewer players than teams.")
    for name, skill in players:
        if not isinstance(skill, int) or skill not in (1, 2, 3):
            raise ValueError(f"Invalid skill for player '{name}': {skill}")
        if not str(name).strip():
            raise ValueError("Player name cannot be empty.")


def _group_by_tier(players: List[Player]) -> Dict[Skill, List[str]]:
    tiers = {1: [], 2: [], 3: []}
    for name, skill in players:
        tiers[skill].append(name)
    return tiers


def _snake_order(n: int, forward: bool = True) -> List[int]:
    return list(range(n)) if forward else list(range(n - 1, -1, -1))


def _target_team_sizes(total_players: int, n_teams: int) -> List[int]:
    base = total_players // n_teams
    extra = total_players % n_teams
    return [base + (1 if i < extra else 0) for i in range(n_teams)]


def pick_teams(players: List[Player], n_teams: int, seed: Optional[int] = None) -> List[Dict]:
    _validate(players, n_teams)
    rng = random.Random(seed)

    teams = []
    for i in range(n_teams):
        teams.append({
            "name": f"Team {i + 1}",
            "players": [],
            "counts": {1: 0, 2: 0, 3: 0},
            "score": 0
        })

    tiers = _group_by_tier(players)
    target_sizes = _target_team_sizes(len(players), n_teams)

    for skill in (1, 2, 3):
        names = tiers[skill][:]
        rng.shuffle(names)

        capacities = [target_sizes[i] - len(teams[i]["players"]) for i in range(n_teams)]
        total = len(names)
        base = total // n_teams
        extra = total % n_teams

        order = _snake_order(n_teams, forward=(skill % 2 == 1))

        desired = [base] * n_teams
        for i in range(extra):
            desired[order[i]] += 1

        targets = [min(desired[i], capacities[i]) for i in range(n_teams)]
        leftover = total - sum(targets)

        if leftover > 0:
            def priority_iter():
                rem_caps = [(i, capacities[i] - targets[i]) for i in range(n_teams)]
                rank = {t: idx for idx, t in enumerate(order)}
                rem_caps.sort(key=lambda x: (-x[1], rank[x[0]]))
                return [i for i, rem in rem_caps if rem > 0]

            while leftover > 0:
                candidates = priority_iter()
                if not candidates:
                    break
                for idx in candidates:
                    if leftover == 0:
                        break
                    targets[idx] += 1
                    leftover -= 1

        idx = 0
        for team_idx in order:
            take = targets[team_idx]
            for _ in range(take):
                if idx >= total:
                    break
                player_name = names[idx]
                teams[team_idx]["players"].append((player_name, skill))
                teams[team_idx]["counts"][skill] += 1
                teams[team_idx]["score"] += WEIGHTS[skill]
                idx += 1

    def pop_lowest(team: Dict):
        for sk in (3, 2, 1):
            for i, (nm, s) in enumerate(team["players"]):
                if s == sk:
                    team["players"].pop(i)
                    team["counts"][s] -= 1
                    team["score"] -= WEIGHTS[s]
                    return nm, s
        return None

    changed = True
    while changed:
        changed = False
        over = [i for i in range(n_teams) if len(teams[i]["players"]) > target_sizes[i]]
        under = [i for i in range(n_teams) if len(teams[i]["players"]) < target_sizes[i]]

        if not over or not under:
            break

        over.sort(key=lambda i: len(teams[i]["players"]) - target_sizes[i], reverse=True)
        under.sort(key=lambda i: target_sizes[i] - len(teams[i]["players"]), reverse=True)

        src = over[0]
        dst = under[0]

        mv = pop_lowest(teams[src])
        if mv:
            nm, sk = mv
            teams[dst]["players"].append((nm, sk))
            teams[dst]["counts"][sk] += 1
            teams[dst]["score"] += WEIGHTS[sk]
            changed = True

    for t in teams:
        t["players"].sort(key=lambda p: (p[1], p[0].lower()))

    return teams
