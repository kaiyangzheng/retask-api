# Retasker - A simple automated and social spaced repetition application

# Overall Goals

- Allow users to better study material with spaced repetition
- Create a social study space where users can interact and study with others
- Use analytical methods to aid the user in studying

As Ebbinghaus put it:

> ***“With any considerable number of repetitions, a suitable distribution of them over a space of time is decidedly more advantageous than the massing of them at a single time.”***
>

---

# Backend

- [ ]  Social network
- [x]  Task goals
- [x]  add endpoints to get task info, stats, and improvement
    - [ ]  remove calculations from frontend when done
- [x]  refactor
    - [x]  rework APIViews to be not as clunky/messy
    - [ ]  ManyToMany field - display data not id
- [ ]  rewrite task stats algorithm
- [ ]  web sockets for real time chat