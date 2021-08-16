# MongoDB 설계
## MongoDB - data modeling
- schema 디자인 할 때 고려사항
  - 사용자 요구 (User Requirement) 에 따라 schema를 디자인한다.
  - 객체들을 함께사용하게 된다면 한 Document에 합쳐서 사용한다. (예: 게시물-덧글 과의 관계)
  - 그렇지 않으면 따로 사용한다 (그리고 join 을 사용하지 않는걸 확실히 해둔다)
  - 읽을때 join 하는게아니라 데이터를 작성 할 때 join 한다.

## Document 관계 데이터 저장 유형
### Embedded
- 2가지 종류의 Document가 있을 때, 1개의 Document 데이터를 다른 Document key의 value에 저장
- 다음은 2가지 종류의 Person, Address Document가 있음
~~~
// Person 
{
   _id: "joe",
   name: "Joe Bookreader"
}

// Address
{
   pataron_id: "joe",
   street: "123 Fake Street",
   city: "Faketon",
   state: "MA",
   zip: "12345"
}
~~~
- 위의 Document를 Embedded 방식으로 관계를 저장하면 다음과 같음
~~~
// Person 
{
   _id: "joe",
   name: "Joe Bookreader",
   address: {
      street: "123 Fake Street",
      city: "Faketon",
      state: "MA",
      zip: "12345"
  }
}

// Address
{
   pataron_id: "joe",
   street: "123 Fake Street",
   city: "Faketon",
   state: "MA",
   zip: "12345"
}
~~~

### Reference
- Document 자체를 통째로 저장하는것이 아니라 참조 할 수 있도록 ID를 저장하는 것
~~~
// Publisher
{
   _id: "oreilly",
   name: "O'Reilly Media",
   founded: 1980,
   location: "CA"
}

// Book
{
   _id: 123456789,
   title: "MongoDB: The Definitive Guide",
   author: [ "Kristina Chodorow", "Mike Dirolf" ],
   published_date: ISODate("2010-09-24"),
   pages: 216,
   language: "English",

   publisher_id: "oreilly" // <- Publisher._id
}
~~~

### Embedded vs Reference
- one-to-many 일 때, 개발의 편의성 관점에서는 embedded, 성능의 효율성 관점에서는 reference 방식 사용
- 서비스의 초기에는 개발의 편의성과 효율성에 초점을 두고 진행해야 개발의 속도에 조금이나마 도움이 될 것이라 생각됨


## data modeling 설계
- 각 site 별로 collection 생성
~~~
{
 _id: POST_ID,
 site: 번개장터,
 title: 애플워치 판매합니다,
 price: 15,000원,
 time: yyyy-mm-dd:HH:MM,
 content: "새제품 입니다"
 like: 20
 Attension: 69
 location: "서울특별시"
}
~~~