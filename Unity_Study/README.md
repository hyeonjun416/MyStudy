# 이상한 백과사전 - 리메이크버젼
## 단축키 - 몰랐거나 까먹은 것 위주
1. V + 자리변경 : 마우스와 가까운 부분에 기즈모 생김 (스내핑 기능) - 꼭짓점을 붙일 때까지
2. Ctrl + Shift + C : 콘솔 뷰
3. Ctrl + Shift + p : 게임을 일시 정지합니다
## 충돌 (Collider)
### 성질 및 정의
1. 충돌메세지를 발생시키는 것은 리지드바디 컴포넌트임
-> 고로 충돌 중인 게임 오브젝트 중에서 **최소 하나의 게임 오브젝트는 리지드바디 컴포넌트를 가지고 있어야함**
2. 게임 오브젝트와 컴포넌트는 충돌 종류에 따라 OnTrigger 혹은 OnCollision 메시지를 받음
3. Trigger는 Collider를 매개변수로 사용하고, Collision은 Collision을 매개변수로 사용함
    * Collision 요소 안에 Collider가 있음
    * Collider 자체는 충돌한 게임 오브젝트의 컴포넌트
#### <span style="color:red"> OnCollision </span>계열 : 일반 충돌
* 일반적인 콜라이더를 가진 두 게임 오브젝트가 충돌할 때 자동으로 실행
* 서로 통과하지 않고 밀어냄
1. OnCollisionEnter : 충돌한 순간
2. OnCollisionStay : 충돌하는 동안
3. OnCollisionExit : 충돌했다가 분리되는 순간
#### OnTrigger 계열 : 트리거 충돌
* 충돌한 두 게임 오브젝트의 콜라이더 중 최소 하나가 트리거 콜라이더라면 자동 실행
* 두 게임 오브젝트가 충돌했을 때 서로 그대로 통과
* 자신이 트리거가 아니더라도 충돌 대상이 트리거라면 실행됨
1. OnTriggerEnter : 충돌한 순간
2. OnTriggerStay : 충돌하는 동안
3. OnTriggerExit : 충돌했다가 분리되는 순간



