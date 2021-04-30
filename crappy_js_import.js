let c = ;


const skill_1 = document.querySelector('[aria-label="第一スキル"]');
const level_1 = document.querySelector('[aria-label="第一スキルポイント"]');
const skill_2 = document.querySelector('[aria-label="第二スキル"]');
const level_2 = document.querySelector('[aria-label="第二スキルポイント"]');
const slots = document.querySelector('[aria-label="スロット"]');

let doTheThing = (ca_idx, max) => {
    console.log("Starting", ca_idx)
    ca = c[ca_idx]
    let sl_v = ca['slots'].join('-')
    slots.value = sl_v
    i = 0
    for (let skill in ca['skills']) {
        skill_sel = i == 0 ? skill_1 : skill_2
        level_sel = i == 0 ? level_1 : level_2
        skill
        skill_sel.value = skill
        level_sel.value = ca['skills'][skill]
        i += 1
    }
    temp1.state.sa = skill_1.value
    temp1.state.aa = level_1.value
    temp1.state.ta = skill_2.value
    temp1.state.ba = level_2.value
    temp1.state.ia = ca['slots']
    temp2(temp1)


    skill_1.value = ""
    level_1.value = 0
    skill_2.value = ""
    level_2.value = 0
    slots.value = "0-0-0"
    temp1.state.sa = skill_1.value
    temp1.state.aa = level_1.value
    temp1.state.ta = skill_2.value
    temp1.state.ba = level_2.value
    temp1.state.ia = [0, 0, 0]

    // Not doing a timeout seemed to bug out
    ca_idx+=1
    if (ca_idx < max) {
        setTimeout(() => {
            doTheThing(ca_idx,  max)
        }, 1) 
    }
}

doTheThing(0, c.length)