BASE_PS1=$PS1
AP_PROMPT=$'\n\e[0;31m$ \e[0m';
function ps1 {
  PYPLAYER=$(cat ~/.pyplayer)
  empty=''
  if [[ $PYPLAYER = $empty ]]; then
    ACT_PS1=$BASE_PS1
  else
    ACT_PS1=$BASE_PS1$PYPLAYER$AP_PROMPT
  fi
}

trap ' ps1; PS1=$ACT_PS1; zle reset-prompt; ' USR1
