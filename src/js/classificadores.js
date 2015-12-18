// AJAX com cache transparente (opcional) via localStorage
function ajax(url, cache, callback){
    // Checa se já possui consulta em cache
    if(localStorage[url] && cache){
        callback(JSON.parse(localStorage[url]));
        return;
    }

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            if(cache){
                localStorage[url] = xmlHttp.responseText;
            }
            callback(JSON.parse(xmlHttp.responseText));
        }
    }
    xmlHttp.open('GET', url, true);
    xmlHttp.send(null);
};

function remover(nome){
    ajax('/api/mongodb/classifier/remove?nome=' + nome, false, function(resp_remover){
        document.location.href = '/classificadores.html';
    });
}

document.querySelector('#brand').onclick = function(){
    document.location.href = '/';
}

/*** Variáveis ***/
var dados_classificadores = document.querySelector('#dados_classificadores');
var input_nome = document.querySelector('#input_nome');
var txt_categorias = document.querySelector('#txt_categorias');
var btn_adicionar = document.querySelector('#btn_adicionar');

// Obtém as informações sobre os classificadores
ajax('/api/mongodb/classifiers/info', false, function(resp_classif){    

    for(var c in resp_classif.info){
        var classif = resp_classif.info[c];
        var html = '<div>';

        if(classif.nome != 'sentimentos'){
            html += '<i class="material-icons" onclick="remover(\'' + classif.nome + '\')">delete</i>';
        }

        html += '<p class="sent">' + classif.nome.toUpperCase() + '</p>';
        html += '<p class="tam">' + classif.tamanho + ' bytes</p>';
        html += '<p class="cat"><strong>Categorias:</strong> ' + classif.categorias + '</p>';
        html += '</div>';

        dados_classificadores.innerHTML += html;
    }


    // Evento de clique o botão para adicionar categoria
    btn_adicionar.onclick = function(){
        var nome_classificador = input_nome.value;
        var categorias = txt_categorias.value.split('\n');

        // valida os campos
        if(!/\S/.test(nome_classificador) || !/\S/.test(categorias) || categorias.length == 1){
            return;
        }

        // Instancia o novo classificador
        var classifier = bayes.exports();
        for(var c in categorias){
            classifier.learn('', categorias[c]);
        }

        ajax('/api/mongodb/classifier/new?nome=' + nome_classificador + '&dados=' + classifier.toJson(), false, function(resp_add){
            document.location.href = '/classificadores.html';
        });

    };

});