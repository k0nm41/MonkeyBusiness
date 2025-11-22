from time import time

import config

from fastapi import APIRouter, Request, Response

from core_common import core_process_request, core_prepare_response, E

router = APIRouter(tags=["local", "local2"])
router.model_whitelist = ["LDJ"]


@router.post("/{prefix}/{gameinfo}/{IIDXver}gameSystem/systemInfo")
async def iidx_gamesystem_systeminfo(IIDXver: str, request: Request):
    request_info = await core_process_request(request)
    game_version = request_info["game_version"]

    unlock = ()
    # force unlock LM exclusives to complete unlock all songs server side
    # this makes LM exclusive folder disappear, so just use hex edits
    # unlock = (30106, 31084, 30077, 31085, 30107, 30028, 30076, 31083, 30098)

    current_time = round(time())

    response = E.response(
        E(
            f"{IIDXver}gameSystem",
            # E.option_2pp(),
            *[
                E.music_open(
                    E.music_id(mid, __type="s32"),
                    E.kind(0, __type="s32"),
                )
                for mid in unlock
            ],
            *[
                E.arena_reward(
                    E.index(unlock.index(mid), __type="s32"),
                    E.cube_num((unlock.index(mid) + 1) * 50, __type="s32"),
                    E.kind(0, __type="s32"),
                    E.value(mid, __type="str"),
                )
                for mid in unlock
            ],
            *[
                E.arena_music_difficult(
                    E.play_style(sp_dp, __type="s32"),
                    E.arena_class(arena_class, __type="s32"),
                    E.low_difficult(8, __type="s32"),
                    E.high_difficult(12, __type="s32"),
                    E.is_leggendaria(1, __type="bool"),
                    E.force_music_list_id(0, __type="s32"),
                )
                for sp_dp in (0, 1)
                for arena_class in range(20)
            ],
            *[
                E.arena_cpu_define(
                    E.play_style(sp_dp, __type="s32"),
                    E.arena_class(arena_class, __type="s32"),
                    E.grade_id(18, __type="s32"),
                    E.low_music_difficult(8, __type="s32"),
                    E.high_music_difficult(12, __type="s32"),
                    E.is_leggendaria(0, __type="bool"),
                )
                for sp_dp in (0, 1)
                for arena_class in range(20)
            ],
            *[
                E.maching_class_range(
                    E.play_style(sp_dp, __type="s32"),
                    E.matching_class(arena_class, __type="s32"),
                    E.low_arena_class(arena_class, __type="s32"),
                    E.high_arena_class(arena_class, __type="s32"),
                )
                for sp_dp in (0, 1)
                for arena_class in range(20)
            ],
        )
    )

    courses = {
        31: {
            0: {
                15: [ 25090, 23068, 19004, 29045 ],
                16: [ 23005, 27078, 22065, 27060 ],
                17: [ 29007, 26108, 19002, 18004 ],
                18: [ 25007, 18032, 16020, 12004 ], 
            },
            1: {
                15: [ 15032, 29033, 27092, 30020 ],
                16: [ 10028, 26070, 28091, 23075 ],
                17: [ 26012, 28002, 17017, 28005 ],
                18: [ 28008, 15001, 19002, 9028 ],
            },
        },
        32: {
            0: {
                15: [ 19022, 30033, 27013, 29045 ],
                16: [ 27034, 24023, 16009, 25085 ],
                17: [ 26087, 19002, 29050, 30024 ],
                18: [ 30052, 18032, 16020, 12004 ],
            },
            1: {
                15: [ 12002, 31063, 23046, 30020 ],
                16: [ 26106, 14021, 29052, 23075 ],
                17: [ 29042, 26043, 17017, 28005 ],
                18: [ 25007, 29017, 19002, 9028 ],
            },
        },
    }

    resp_append = []
    if game_version in courses:
        resp_append = [
            *[E.grade_course(
                E.play_style(spdp, __type="s32"),
                E.grade_id(course, __type="s32"),
                E.music_id_0(courses[game_version][spdp][course][0], __type="s32"),
                E.class_id_0(3, __type="s32"),
                E.music_id_1(courses[game_version][spdp][course][1], __type="s32"),
                E.class_id_1(3, __type="s32"),
                E.music_id_2(courses[game_version][spdp][course][2], __type="s32"),
                E.class_id_2(3, __type="s32"),
                E.music_id_3(courses[game_version][spdp][course][3], __type="s32"),
                E.class_id_3(3, __type="s32"),
                E.is_valid(1, __type="bool"),
            )
            for spdp in courses[game_version]
            for course in courses[game_version][spdp]
            ],
        ]
        for r in resp_append:
            response.find(f"{IIDXver}gameSystem").append(r)
        resp_append[:] = []

    if game_version == 33:
        resp_append = [
            E.arena_schedule(
                E.season(1, __type="u8"),
                E.phase(4, __type="u8"),
                E.rule_type(0, __type="u8"),
                E.start(current_time - 600, __type="u32"),
                E.end(current_time + 600, __type="u32"),
            ),
            #E.Event1Phase(val=0),
            E.isNewSongAnother12OpenFlg(val=1),
            #E.isKiwamiOpenFlg(val=1),
            #E.WorldTourismOpenList(val=-1),
            E.OldBPLBattleOpenPhase(val=1),
            #E.BPLBattleOpenPhase(val=3),
            E.beat(val=0),
        ]
    elif game_version == 32:
        resp_append = [
            E.arena_schedule(
                E.season(1, __type="u8"),
                E.phase(4, __type="u8"),
                E.rule_type(0, __type="u8"),
                E.start(current_time - 600, __type="u32"),
                E.end(current_time + 600, __type="u32"),
            ),
            E.Event1Phase(val=0),
            E.isNewSongAnother12OpenFlg(val=1),
            E.isKiwamiOpenFlg(val=1),
            E.WorldTourismOpenList(val=-1),
            E.OldBPLBattleOpenPhase(val=3),
            E.BPLBattleOpenPhase(val=3),
        ]
    elif game_version == 31:
        resp_append = [
            E.arena_schedule(
                E.phase(3, __type="u8"),
                E.rule_type(0, __type="u8"),
                E.start(current_time - 600, __type="u32"),
                E.end(current_time + 600, __type="u32"),
            ),
            E.CommonBossPhase(val=0),
            E.Event1Phase(val=0),
            E.Event1Value(val=0),
            E.Event2Phase(val=0),
            E.ExtraBossEventPhase(val=0),
            E.isNewSongAnother12OpenFlg(val=1),
            E.isKiwamiOpenFlg(val=1),
            E.WorldTourismOpenList(val=-1),
            E.OldBPLBattleOpenPhase(val=3),
            E.BPLBattleOpenPhase(val=3),
            E.UnlockLeggendaria(val=1),
            E.Event1AllPlayerTotalGetMetron(val=0),
        ]
    elif game_version == 30:
        resp_append = [
            E.arena_schedule(
                E.phase(3, __type="u8"),
                E.start(current_time - 600, __type="u32"),
                E.end(current_time + 600, __type="u32"),
            ),
            E.CommonBossPhase(val=0),
            E.Event1InternalPhase(val=0),
            E.ExtraBossEventPhase(val=0),
            E.isNewSongAnother12OpenFlg(val=1),
            E.gradeOpenPhase(val=2),
            E.isEiseiOpenFlg(val=1),
            E.WorldTourismOpenList(val=-1),
            E.BPLBattleOpenPhase(val=3),
        ]
    elif game_version == 29:
        resp_append = [
            E.arena_schedule(
                E.phase(3, __type="u8"),
                E.start(current_time - 600, __type="u32"),
                E.end(current_time + 600, __type="u32"),
            ),
            E.CommonBossPhase(val=0),
            E.Event1InternalPhase(val=0),
            E.ExtraBossEventPhase(val=0),
            E.isNewSongAnother12OpenFlg(val=1),
            E.gradeOpenPhase(val=2),
            E.isEiseiOpenFlg(val=1),
            E.WorldTourismOpenList(val=-1),
            E.BPLBattleOpenPhase(val=2),
        ]

    if resp_append != []:
        for r in resp_append:
            response.find(f"{IIDXver}gameSystem").append(r)

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)
