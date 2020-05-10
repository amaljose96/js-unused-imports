export function uniquePush(list,newItem){
    let map={};
    list.forEach(listItem=>{
        map[JSON.stringify(listItem)]=listItem;
    })
    map[JSON.stringify(newItem)]=newItem;
    return Object.values(map);
}