# MongoDB 명령어 정리
- DataBase 생성
~~~
$ use transaction_data   #- transaction_data db 생성
$ db                     #- 현재 사용중인 db 확인
$ show dbs               #- database list 확인
~~~
- Database 제거
~~~
$ use transaction_data   #- 제거하려는 db 선택해 주어야 함
$ db.dropDatabase();     #- db 제거
~~~
- Collection 생성
  - `name` : 생성하려는 컬렉션의 이름
  - `option` : document 타입으로 구성된 해당 컬렉션의 설정값 
    - `capped`, Boolean, True시 고정된 크기를 가진 컬렉션으로서, size가 초과되면 가장 오래된 데이터를 덮어씀
    - `autoIndex` : Boolean, 이 값을 True로 설정하면, _id 필드에 index를 자동으로 생성
    - `size` : number, collection의 최대사이즈를 ~bytes로 지정
    - `max` : 해당 컬렉션에 추가 할 수 있는 최대 개수
~~~
db.createCollection(name, [options])
~~~
~~~
$ db.createCollection("books") # 옵션 없이 collection 생성
$ db.createCollection("articles", { 
$    capped: true,
$    size: 6142800,
$    max: 10000
$    })

# creatCollection()을 따로 사용하지 않아도 document를 추가하면 자동 컬렉션 생성
$ db.people.insert({"name": "velopert"})

# 내가 만든 collection list 확인
$ show collections

# collection 제거
$ use test
$ show collections
$ db.people.drop()
$ show collections
~~~
- Document 추가
  - 명령어 수행전 데이터를 추가 할 데이터베이스 선택 필요
  - 배열형식의 인자를 전달해주면 여러 다큐먼트를 동시에 추가 할 수 있음 
~~~
$ db.books.insert({"name": "NodeJS Guide", "author": "Velopert"})

$ db.books.insert([
$     {"name": "Book1", "author": "Velopert"},
$     {"name": "Book2", "author": "Velopert"}
$     ]);
~~~
- Document 제거
  - `criteria`, document , 삭제 할 데이터의 기준 값. 이 값이 {}이면 모든 데이터를 제거
  - `justOne`, boolean, 선택적 매개변수, 이 값이 true면 1개의 다큐먼트만 제거. 해당 매개변수가 생략되면 기본값은 false, criteria에 해당되는 모든 다큐먼트를 제거함
- 초보 일때는 반드시 `find()`를 통해 확인하는 것을 습관화 해야 함
~~~
$ db.books.find({"name": "Book1"})
$ db.books.remove({"name": "Book1"})
~~~
- Document 조회
  - `query`, document,  optional, 다큐먼트를 조회할 때 기준을 정함. 기준 필요 없으면 {} 전달
  - `projection`, document, Optional, 다큐먼트를 조회할 때 보여질 field를 정함  
  - 반환값 : cursor
    - Document 들을 선택하여 cursor를 반환. cursor는 query 요청의 결과값을 가리키는 pointer
    - cursor 객체를 통하여 보이는 데이터의 수를 제한 할 수 있고, 데이터를 sort 할 수도 있음
    - 이는 10분동안 사용하지 않으면 만료됨
- 모든 다큐먼트 조회
~~~
$ db.articles.find()
~~~
- 다큐먼트를 깔끔하게 조회
~~~
$ db.articles.find().pretty()
~~~
- writer 값이 Velopert인 document 조회
~~~
$ db.articles.find({'writer':'Velopert'}).pretty()
~~~
- likes 값이 30 이하인 Document 조회
~~~
$ db.articles.find({"likes": {$lte: 30}}).pretty()
~~~

### 비교 연산자
- `$eq`, 주어진 값과 같은 값
- `$gt`, 주어진 값보다 큰 값
- `$gte`, 주어진 값보다 크거나 같은 값
- `$lt`, 주어진 값보다 작은 값
- `$lte`, 주어진 값보다 작거나 같은 값
- `$ne`, 주어진 값과 일치하지 않은 값
- `$in`, 주어진 배열안에 속하지 않는 값
- `$nin`, 주어진 배열 안에 속하지 않은 값
- likes 값이 10보다 크고 30보다 작은 Document 조회
~~~
$ db.articles.find({'likes':{$gt: 10, $lt: 30}}).pretty()
~~~
-  writer 값이 배열 [“Alpha”, “Bravo”] 안에 속하는 값인 Document 조회
~~~
$ db.articles.find({'writer': {$in: ['Alpha', 'Bravo']}})
~~~

### 논리 연산자
- `$or`, `$and`, `$not`, `$nor`
- title 값이 “article01” 이거나, writer 값이 “Alpha” 인 Document 조회
~~~
$ db.articles.find({$or:[{"title":"article01"}, {"writer":"Alpha"}]}).pretty()
~~~
- writer 값이 “Velopert” 이고 likes 값이 10 미만인 Document 조회
~~~
$ db.articles.find( { $and: [ { "writer": "Velopert" }, { "likes": { $lt: 10 } } ] } )
$ db.articles.find({"writer":"Velopert", "likes":{$lt:10}})
~~~

### regex 연산자
- regex 연산자를 통해 Document를 정규식을 통해 찾을 수 있음
- 이 연산자는 다음과 같이 사용
~~~
{ <field>: { $regex: /pattern/, $options: '<options>' } }
{ <field>: { $regex: 'pattern', $options: '<options>' } }
{ <field>: { $regex: /pattern/<options> } }
{ <field>: /pattern/<options> }
~~~
- `i`, 대소문자 무시
- `m`, 정규식에서 anchor(^)를 사용할 때 값에 \n이 있다면 무력화
- `x`, 정규식안에있는 whitespace를 모두 무시
- `s`, dot(.) 사용할 때 \n를 포함해서 모두 무시
- <b>article[0-2]</b>에 일치하는 값이 title에 있는 Document 조회
~~~
db.articles.find({'title':/article[0-2]/}).pretty()
~~~

### where 연산자
- `$where` 연산자를 통해서 javascript expression을 사용할 수 있음
- comments field가 비어있는 Document 조회
~~~
db.articles.find({$where: "this.comments.length == 0"})
~~~

### elemMatch 연산자
- Embedded Documents 배열을 쿼리할 때 사용
- comments 중 “Charlie” 가 작성한 덧글이 있는 Document 조회
~~~
db.articles.find({"comments": {$elemMatch : {"name": "Charlie"}}})
~~~
- Embedded Document 배열이 아니라, 아래 Document의 "name"처럼 한개의 Embedded Document 일 시에는  
~~~
{
    "username": "velopert",
    "name": { "first": "M.J.", "last": "K."},
    "language": ["korean", "english", "chinese"]
}
~~~
- 다음과 같이 쿼리함
~~~
db.articles.find({"name.first":"M.J."})
~~~
- Document의 배열이 아니라, 그냥 단순 배열([])일 시는 다음과 같이 쿼리함
~~~
db.users.find({"language": "korean"})
~~~

### projection
- `find()` 메소드의 두번째 parameter인 projection에 대하여 알아보도록 하자
- 쿼리의 결과값에서 보여질 field를 정하는 것
- article의 title과 content 만 조회
~~~
db.articles.find({},{_id:false, "title":true, "content":true})
~~~

### silce 연산자
- projector 연산자 중 $slice 연산자는 Embedded Document 배열을 읽을 때 limit 설정을 함
- title 값이 article03인 Document 에서 덧글은 하나만 보이게 출력
~~~
db.articles.find({"title":"article03"}, {comments:{$slice : 1}}).pretty()
~~~
- slice가 없었더라면 comment가 2개가 나왔을테지만, 1개로 제한을 두었기에 한개만 출력하게 됨

### elemMatch 연산자
- comments 중 "Charlie"가 작성한 덧글이 있는 Document 조회를 했을 때, 게시물 제목과 Charlie의 덧글부분만 읽고 싶을 때
- `$elemMatch` 연산자를 projection 연산자로 사용하면 이를 구현 할 수 있습니다
~~~
db.articles.find(
  {
  "comments": {
      $elemMatch: {"name": "Charlie"}
    }
  },
  {
    "title": true,
    "comments": {
      $elemMatch: { "name": "Charlie" }
    },
  }
)
~~~

## 실습2 - sort(), limit(), skip()
- 단순히 `find()` 메소드를 사용하면 criteria에 일치하는 모든 document들을 출력해주기 때문에, 예를들어 페이지 같은 기능을 사용한다면 불적합
- `find()` 메소드 자체에 어디부터 어디까지 불러오겠다라고 설정하는 매개변수는 따로 없음
- `find()` 메소드를 사용했을 때 cursor 형태의 결과값을 반환하는데, 이 객체가 가지고 있는 `limit()`메소드와 `skip()`메소드를 통하여 보이는 출력물의 개수를 제한할 수 있고, `sort()` 메소드를 사용하여 데이터를 순서대로 나열 할 수 있음
- 원할한 실습을 위하여 다음의 sample code를 입력합니다
~~~
db.orders.insert([
    { "_id": 1, "item": { "category": "cake", "type": "chiffon" }, "amount": 10 },
    { "_id": 2, "item": { "category": "cookies", "type": "chocolate chip" }, "amount": 50 },
    { "_id": 3, "item": { "category": "cookies", "type": "chocolate chip" }, "amount": 15 },
    { "_id": 4, "item": { "category": "cake", "type": "lemon" }, "amount": 30 },
    { "_id": 5, "item": { "category": "cake", "type": "carrot" }, "amount": 20 },
    { "_id": 6, "item": { "category": "brownies", "type": "blondie" }, "amount": 10 }  
  ]
)
~~~

### cursor.sort()
- 데이터 정렬시 사용. 매개변수로 어떤 KEY를 사용하여 정렬할 지 알려주는 document를 전달함
~~~
db.orders.find().sort({"_id": 1})
db.orders.find().sort({"amount": 1, "_id": -1})
~~~

### cursor.limit(value)
- 이 메소드는 출력할 데이터 갯수를 제한할 때 사용함. value 파라미터는 출력 할 갯수 값
~~~
db.orders.find().limit(3)
~~~

### cursor.skip(value)
- 출력 할 데이터의 시작부분을 설정할 때 사용

### 응용
- order를 최신순으로 한 페이지당 2개씩 나타냄
~~~
var showPage = function(page){
  return db.orders.find().sort({"_id": -1}).skip((page-1)*2).limit(2);
}
~~~

### update 
- document를 수정하는 update() 메소드
- 메소드의 구조는 다음과 같음
~~~
db.collection.update(
  <query>,
  <update>,
  { 
    update: <boolean>,
    multi: <boolean>,
    writeConcern: <document>
  }
)
~~~
- update() 메소드의 기본 옵션으로는 단 하나의 document를 수정
- `query`, document, 업데이트 할 document의 criteria 를 정함. find() 메소드에서 사용하는 query와 같음
- `update`, document, document에 적용할 변동사항
- `upsert`, boolean, Optional. 값이 true로 설정되면 query한 document가 없을 경우, 새로운 document 추가
- `multi`, Optional(기본값 false), 이 값이 true로 설정되면, 여러개의 document를 수정
- `writeConcern`, Optional, wtimeout 등 document 업데이트 할 때 필요한 설정값. 
~~~
db.people.insert([
    { name: "Abet", age: 19 },
    { name: "Betty", age: 20 },
    { name: "Charlie", age: 23, skills: [ "mongodb", "nodejs"] },
    { name: "David", age: 23, score: 20 }
])
~~~
- 특정 field 업데이트 하기
~~~
db.people.update({"name": "Abet"}, {$set: {age: 20}})
~~~

- document를 Replace 하기
~~~
db.people.update({name: "Betty"}, {"name": "Betty 2nd", age: 1})
~~~

- 특정 Field를 제거하기
~~~
# David document의 score field를 제거
db.people.update({name: "David"}, {$unset: {score: 1}})
~~~

- criteria에 해당되는 document가 존재하지 않는다면 새로 추가  
~~~
db.people.update({name: "Elly"}, {name:"Elly", age: 17}, {upsert: true})
~~~

- 여러 document의 특정 field를 수정
~~~
# age가 20 보다 낮거나 같은 document의 score를 10으로 설정
$ db.people.update(
$  {age: {$lte: 20}},
$  {$set: {score: 10}}, 
$  {multi: true}
$ )
~~~

- 배열에 값 추가하기
~~~
# Charlie document의 
db.people.update(
  {name: "Charlie"},
  { $push: {skills: "angularjs"}}
)
~~~
- 배열에 값 여러개 추가하기 + 오름차순 정렬하기
~~~
# Charlie document의 skills에 "c++" 와 "java" 를 추가하고 알파벳순으로 정렬
db.people.update(
  {name: "Charlie"},
  {$push: {
    skills: {
      $each: ["c++", "java"],
      $sort: 1 
      }
    }
  }
)
~~~
- 배열이 document의 배열이고, 특정 embedded document의 특정 field에 따라서 정렬을 할 때는 다음과 같이 설정하면 됨
~~~
$sort: {KEY: 1}
~~~
- 배열에서 여러개 값 제거하기
~~~
db.people.update(
  {name: "Charlie"},
  {$pull: {skills: { $in: ["angularjs", "java"] } } }
)
~~~

## 나머지 공부 
### 실습1
~~~
db.articles.insert([
    {
        "title" : "article01",
        "content" : "content01",
        "writer" : "Velopert",
        "likes" : 0,
        "comments" : [ ]
    },
    {
        "title" : "article02",
        "content" : "content02",
        "writer" : "Alpha",
        "likes" : 23,
        "comments" : [
                {
                        "name" : "Bravo",
                        "message" : "Hey Man!"
                }
        ]
    },
    {
        "title" : "article03",
        "content" : "content03",
        "writer" : "Bravo",
        "likes" : 40,
        "comments" : [
                {
                        "name" : "Charlie",
                        "message" : "Hey Man!"
                },
                {
                        "name" : "Delta",
                        "message" : "Hey Man!"
                }
        ]
    }
])
~~~
- 모든 다큐먼트 조회
~~~
db.articles.find()
~~~

- 다큐먼트를 예쁘게 깔끔하게 조회
~~~
db.articles.find().pretty()
~~~

- writer 값이  “Velopert” 인 Document 조회
~~~
db.articles.find({"writer":"Velopert"}).pretty()
~~~

- likes 값이 30 이하인 Document 조회
~~~
db.articles.find({"likes":{$lte: 30}}).pretty()
~~~

- likes 값이 10보다 크고 30보다 작은 Document 조회
~~~
db.articles.find({
  $and:[{"likes": {$lt: 30}}  , {"likes": {$gt: 10}}]
}).pretty()
~~~

- title 값이 “article01” 이거나, writer 값이 “Alpha” 인 Document 조회
~~~
db.articles.find({
  $or:[{"title":"article01"} , {"writer":"Alpha"}]
}).pretty()
~~~

- writer 값이 “Velopert” 이고 likes 값이 10 미만인 Document 조회
~~~
db.articles.find({
  $and:[{"writer":"Velopert"} , {"likes":{$lt: 10}}]
}).pretty()
~~~

- 정규식 article0[1-2] 에 일치하는 값이 title 에 있는 Document 조회
~~~
db.articles.find({'title':/article[0-2]/}).pretty()
~~~

- comments field 가 비어있는 Document 조회
~~~
db.articles.find({$where: "this.comments.length == 0"})
~~~

- comments 중 “Charlie” 가 작성한 덧글이 있는 Document 조회
~~~
db.articles.find({
  "comments": {
    $elemMatch: {"name":"Charlie"}
  }
})
~~~

- article의 title과 content 만 조회
~~~
db.articles.find({}, {"title":true, "content":true})
~~~

- title 값이 article03 인 Document 에서 덧글은 하나만 보이게 출력
~~~
db.articles.find({"title":"article03"}, {comments:{$slice: 1}})
~~~

- “ comments 중 “Charlie” 가 작성한 덧글이 있는 Document 조회 ” 를 했을때, 게시물 제목과 Charlie의 덧글부분만 읽고싶을 때?

- comments 중 “Charlie” 가 작성한 덧글이 있는 Document 중 제목, 그리고 Charlie의 덧글만 조회
~~~
db.articles.find(
  {
    "comments": {
      $elemMatch: {"name": "Charlie"}
    }
},
{
  "title": true,
  "comments": {
    $elemMatch: {"name":"Charlie"}
  }
}
).pretty()
~~~

### 실습2
~~~
db.orders.insert(
  [
    { "_id": 1, "item": { "category": "cake", "type": "chiffon" }, "amount": 10 },
    { "_id": 2, "item": { "category": "cookies", "type": "chocolate chip" }, "amount": 50 },
    { "_id": 3, "item": { "category": "cookies", "type": "chocolate chip" }, "amount": 15 },
    { "_id": 4, "item": { "category": "cake", "type": "lemon" }, "amount": 30 },
    { "_id": 5, "item": { "category": "cake", "type": "carrot" }, "amount": 20 },
    { "_id": 6, "item": { "category": "brownies", "type": "blondie" }, "amount": 10 }
  ]
)
- _id 의 값을 사용하여 오름차순으로 정렬하기
~~~
db.orders.find().sort({"_id" : 1})
~~~

- amount 값을 사용하여 오름차순으로 정렬하고, 정렬한 값에서 id 값은 내림차순으로 정렬하기
db.orders.find().sort({"amount": 1, "_id": -1})

- 출력 할 갯수를 3개로 제한하기
db.orders.find().limit(3)

- 2개의 데이터를 생략하고 그 다음부터 출력
db.orders.find().skip(2)

- order 를 최신순으로 한 페이지당 2개씩 나타내기
var showPage = function(page){
  return db.orders.find().sort({"_id": -1}).skip((page-1)*2).limit(2)
}

### 실습3
~~~
db.people.insert([
    { name: "Abet", age: 19 },
    { name: "Betty", age: 20 },
    { name: "Charlie", age: 23, skills: [ "mongodb", "nodejs"] },
    { name: "David", age: 23, score: 20 }
])
~~~
- Abet document 의 age를 20으로 변경한다
- Betty document를 새로운 document로 대체한다.
- David document의 score field를 제거한다
- upsert 옵션을 설정하여 Elly document가 존재하지 않으면 새로 추가
- age가 20 보다 낮거나 같은 document의 score를 10으로 설정
- Charlie document의 skills 배열에 "angularjs" 추가
- Charlie document의 skills에 "c++" 와 "java" 를 추가하고 알파벳순으로 정렬
- Charlie document에서 skills 값의 mongodb 제거
- Charlie document에서 skills 배열 중 "angularjs" 와 "java" 제거



## 참고 블로그
https://velopert.com/479
