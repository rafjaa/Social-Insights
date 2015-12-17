/*** Variáveis ***/
var input_busca = document.querySelector('#busca');
var select_classif = document.querySelector('#select_classif');
var btn_buscar = document.querySelector('#btn_buscar');
var p_brand = document.querySelector('#brand');
var span_classif = document.querySelector('#classificadores');
var section_resultados = document.querySelector('#resultados');
var section_graficos = document.querySelector('#graficos');
var ctx_analise = document.getElementById('chart_analise').getContext("2d");
var ctx_impacto = document.getElementById('chart_impacto').getContext("2d");
var grafico_analise = null;
var grafico_impacto = null;
var atualiza_treinamento = null;
var j = null;

var CORES = ['#f78f38', '#ef3b2d', '#5e2c8d', '#bab732', '#f13d2f', '#32728b', '#016aae', '#019f91', '#f78f38', '#ef3b2d', '#5e2c8d', '#bab732', '#f13d2f', '#32728b'];

/*** Funções ***/

// AJAX com cahce transparente (opcional) via localStorage
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

span_classif.onclick = function(){
    document.location.href = '/classificadores.html';
}

p_brand.onclick = function(){
    document.location.href = '/';
}

/*** Recupera os classificadores persistidos no banco ***/
ajax('/api/mongodb/classifiers', false, function(resp_classif){

    // Reconstrói os classificadores
    var classificadores = {};

    for(var c in resp_classif){
        classificadores[c] = bayes.exports.fromJson(resp_classif[c]);

        // Preenche a tag 'select' do formulário
        select_classif.options.add(new Option(c.toUpperCase(), c));
    }

    // Clique em buscar
    btn_buscar.onclick = function(){
        var termo = input_busca.value;

        // Verifica se a busca está vazia ou só com espaços em branco
        if(!/\S/.test(termo)){
            return;
        }

        var id_classif = select_classif.value;

        // Carregando
        section_resultados.innerHTML = '<p style="text-align: center; margin-top: 30px;"><img src="img/carregando.gif"></p>';

        // Consome a API do Twitter
        ajax('/api/twitter/search?q=' + termo, true, function(resp_json){
            var tweets = resp_json.tweets;
            var cont_categorias = {};
            // Inicializa as categorias
            for(var c in classificadores[id_classif].categories){
                cont_categorias[c] = {'cont': 0, 'retweets': 0, 'followers': 0};
            }

            var html = '';
            for(var i in tweets){
                var tweet = tweets[i];
                var classificacao = classificadores[id_classif].categorize(tweet.text);

                cont_categorias[classificacao].cont += 1;
                cont_categorias[classificacao].retweets += (tweet.retweet_count ? tweet.retweet_count : 0);
                cont_categorias[classificacao].followers += (tweet.user.followers_count ? tweet.user.followers_count : 0);

                html += '<div id="tweet" class="animated slideInUp"><strong>' + tweet.user.name + ':</strong> ' + tweet.text;
                html += '<p>' + (tweet.retweet_count ? tweet.retweet_count : 0) + ' retweets, ' + (tweet.user.followers_count ? tweet.user.followers_count : 0) + ' usuários impactados</p>';
                html += '<select onchange="atualiza_treinamento(this);" data-text="' + tweet.text + '">';
                // Lista todas as categorias para que o usuário possa corrigir o treinamento
                for(var c in classificadores[id_classif].categories){
                    if(c == classificacao)
                        html += '<option value="' + c + '" selected>' + c + '</option>';
                    else{
                        html += '<option value="' + c + '">' + c + '</option>';
                    }
                }
                html += '</select></div>';
            }
            section_resultados.innerHTML = html;

            /*** Gráficos ***/
            var dados_pizza = [];
            var cont_cores = 0;
            for(var cat in cont_categorias){
                dados_pizza.push({
                    value: cont_categorias[cat].cont,
                    label: cat.toUpperCase(),
                    color: CORES[cont_cores]
                });
                cont_cores += 1;
            }

            var dados_barra = {labels: [], datasets: [
                {
                    label: "Retweets",
                    fillColor: '#016aae',
                    data: []
                },
                {
                    label: "Seguidores",
                    fillColor: '#019f91',
                    data: []
                }
            ]};

            for(var cat in cont_categorias){
                dados_barra['labels'].push(cat.toUpperCase());
                dados_barra['datasets'][0].data.push(cont_categorias[cat].retweets);
                dados_barra['datasets'][1].data.push(cont_categorias[cat].followers);
            }

            if(grafico_analise){
                grafico_analise.destroy();
            }
            if(grafico_impacto){
                grafico_impacto.destroy();
            }

            section_graficos.style.display = 'block';

            grafico_analise = new Chart(ctx_analise).Doughnut(dados_pizza);
            grafico_impacto = new Chart(ctx_impacto).Bar(dados_barra);
        });
    }; // Clique em buscar

    // Pressionar enter na busca
    input_busca.onkeyup = function(event){
        if(event.keyCode == 13){
            btn_buscar.onclick();
        }
    };

    select_classif.onchange = function(){
        btn_buscar.onclick();
    }

    // Alteração treinamento
    atualiza_treinamento = function(select){
        var id_classif = select_classif.value;
        var nova_categoria = select.value;
        var texto_tweet = select.dataset.text;

        classificadores[id_classif].learn(texto_tweet, nova_categoria);
        j = classificadores[id_classif].toJson();

        //Persiste o novo treinamento
        ajax('/api/mongodb/classifier/update?nome=' + id_classif + '&dados=' + classificadores[id_classif].toJson(), false, function(resp_update){
        });
    }

}); // AJAX classificadores