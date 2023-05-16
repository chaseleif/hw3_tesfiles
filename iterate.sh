#! /bin/bash

if [ -z $1 ] ; then
  echo "Usage: $0 <command>"
  echo "commands:"
  echo "ssh     - print ssh-agent instructions"
  echo "reset   - each repo do  -> rm -rf * ; git reset --hard HEAD ;"
  echo "pull    - eacho repo do -> git pull"
  echo "test    - in assgn dir, rm -rf makefile ./test ; cp -r test . ; print output of make test"
  echo "writeup - prints the writeup in the assignment dir of each repo"
  echo "date    - prints the top date from the git log of each repo"
  echo "cmd     - do a command in each repo level directory"
  echo "print   - prints each repo name"
  exit 0
fi

if [ $1 == "cmd" ] ; then
  declare -a runcmd
  for part in "${@}" ; do
    if [ "$part" == "$1" ] ; then continue ; fi
    if [ "${part// }" == "$part" ] ; then
      runcmd+=("$part")
    else
      runcmd+=("\"$part\"")
    fi
  done
elif [ $1 == "ssh" ] ; then
  echo "do:"
  echo "eval \`ssh-agent\`"
  echo "ssh-add"
  exit 0
fi

### Skip past beginning of the list
skipto=0
skipdir="lastrepo"

declare -A excludedirs
declare -A selectdirs

### only do a partial run, (list the dir names)
dopartial=0
if [ $dopartial == 1 ]; then
  for name in onlythisrepo ; do
    selectdirs["${name}/"]=1
  done
fi

### exclude these dirs (can add additional dirnames)
# always exclude: "." ".." "templates" "tests" "sol"
for name in . .. ; do
  excludedirs["${name}/"]=1
done

# current directory
base=$(dirname $(realpath 0))

cd sp23/

# iterate through the directories
for dir in */ .*/ ; do
  if [ ! -d "$base/sp23/$dir" ] ; then
    continue
  fi
  if [[ ${excludedirs["$dir"]} -ne 1 ]]; then
    if [ $skipto -eq 1 ]; then
      echo $dir
      if [ $dir == "${skipdir}/" ]; then
        skipto=0
      else
        continue
      fi
    fi
    if [ $dopartial == 1 ] && [[ ${selectdirs["$dir"]} -ne 1 ]]; then
      continue
    fi
    cd ${base}/sp23/${dir}
    if ! [ -z "${runcmd}" ]; then
      echo ${dir}
      "${runcmd[@]}"
    elif [ $1 == "print" ]; then
      echo ${dir}
    elif [ $1 == "reset" ]; then
      [ ! -d ".git" ] && echo "No .git, cannot reset: ${dir}" && continue
      echo ${dir}
      rm -rf *
      git reset --hard HEAD
    elif [ $1 == "pull" ]; then
      [ ! -d ".git" ] && echo "No .git, cannot pull: ${dir}" && continue
      echo ${dir}
      git pull
    elif [ $1 == "test" ]; then
      echo "########"
      echo "##################"
      echo "####################################"
      echo ${dir}
      rm -rf test/
      cp -r ${base}/tests/test .
      cp ${base}/tests/Makefile .
      cp ${base}/tests/*.py test/
      make clean && echo ${dir} && make test
      echo "####################################"
      read -n 1 -p "above was ${dir::-1}, press the enter key to continue . . . " dummyval
      clear
    elif [ $1 == "date" ]; then
      [ ! -d ".git" ] && echo "#####
###  No .git, cannot get date: ${dir}
#####
" && continue
      echo ${dir}
      git log | head -n 4 | tail -n 3
    fi
  fi
done

