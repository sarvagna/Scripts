setwd("C:/Users/jhs/Desktop/backup/FY15/GRT/ontology/frameToD3-master")

to_df<-read.table('C:/Users/jhs/Desktop/backup/FY15/GRT/ontology/PO_Dump.txt',header=T,sep="\t")

makeList<-function(x){
  x2 <- dplyr::filter(x, x[1] != "")
  if(ncol(x2)>1){
    listSplit <- split(x2[-1], x2[1], drop = TRUE)
    sapply(names(listSplit),function(y){
      l<-list(makeList(listSplit[[y]]))
      if(length(l)==0){
        l<-list("")
      }
      l
    })
  }
  else{
    sapply(seq(nrow(x2)),function(y){
        l<-list("")
        names(l)<-x2[,1][y]
        l
    })
  }
}

remove_empty_lists <- function(l){
  lapply(l, function(x) if(is.list(x) && length(x)==0) "" else if(is.list(x)) remove_empty_lists(x) else x)
}


to_list<-makeList(to_df[-1])
repaired_list<-remove_empty_lists(to_list)

saveRDS(repaired_list,file="po_list.Rds")
