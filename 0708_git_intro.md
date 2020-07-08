# hello

| a    | b      | c    |
| ---- | ------ | ---- |
| 서연 | 두레기 | 한돌 |

`a=1` code is assignment

```python
def a():
	x = 1
    y = 2
    return x = 1


```

```latex
$$
\begin{align*}
y = y(x,t) &= A e^{i\theta} \\
&= A (\cos \theta + i \sin \theta) \\
&= A (\cos(kx - \omega t) + i \sin(kx - \omega t)) \\
&= A\cos(kx - \omega t) + i A\sin(kx - \omega t)  \\
&= A\cos \Big(\frac{2\pi}{\lambda}x - \frac{2\pi v}{\lambda} t \Big) + i A\sin \Big(\frac{2\pi}{\lambda}x - \frac{2\pi v}{\lambda} t \Big)  \\
&= A\cos \frac{2\pi}{\lambda} (x - v t) + i A\sin \frac{2\pi}{\lambda} (x - v t)
\end{align*}
$$
```





# git intro

## local part



1. 초기화 ` $ git init`

    1. 실제로는 .git/폴더가생성됨

    2.  버전관리가 시작됨

    3. 리포(repository)라고 부름

       

2. 서면 설정

    1. `$ git config  --global user.name "name"`

    2. `$ git config --global user.email "email@mail"`

       

3.  리포의 상태보기 `$ git status`

4. stage 에 올리기 `$ git add`

   1. 특정파일만 올리기

      git add <filename>

   2. 그냥 다 올리기 git add .

5. snapshot(사진)직기`$ git commit `

6. 로그 (사진첩) 보기`$ git log`



# github

1. 원격저장소(remote repository) 생성
2. 로컬 리포 ==> 리모트 리포 연결하기 `$ git remote add origin <url>`
3. 로컬 커밋들을 리모트로 보내기 `$ git push origin master`
4. `$ git push origin master`로 단축 명령 하기 `$ git push -u origin master`
5.  다른 컴퓨터에서 remote repo 받아오기 `$  git clone <url>`
6.  이후 remote repo 변경사항을 local repo에서 반영하기 ` $ git pull`



# TIL 관리 시나리오

1. 멀캠에 온다.

2. `$ git pull`

3. 열공

4. 중간중간 ` git add . ` & `git commit`

5. 집가기전에 `$ git push`

6. 집도착

7. `$ git pull`

8. 복습 및 자습(`git commit`)

9. 마지막으로 `$ git push`

10. 1번으로

    

