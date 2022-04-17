<?php
/*
Plugin Name: Análise de Sentimentos de comentários
Plugin URI: http://devorando.net
Description: Análise de Sentimentos de comentários de posts do wordpress
Version: 0.0.1
Author: Marcos Nunes
Author URI: https://marcosnunes.dev
Licence: GPLv2 or Later
*/


function show_analize() {
    // if(!is_admin()) {
    //     return;
    // }
    global $post;
    $curreent_post = $post->ID;
    $base_url = "http://127.0.0.1:5000";
    $url = $base_url . "/analize/".$curreent_post;

    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

    $r = curl_exec($curl);

    curl_close($curl);

    $resp = json_decode($r);

    if($r) {

    $html = '
    <h4>Sentimentos</h4>

    <div class="row">
    
        <div class="col-6">
        
            <div class="alert alert-success" role="alert">
                Alegria: <strong>' . number_format($resp->sentiments->Alegria, 2, '.', '') . '%</strong></br>
            </div>
            <div class="alert alert-danger" role="alert">
                Medo: <strong>' . number_format($resp->sentiments->Medo, 2, '.', '') . '%</strong></br>
            </div>
            <div class="alert alert-primary" role="alert">
                Indefinido: <strong>' . number_format($resp->sentiments->Indefinido, 2, '.', '') . '%</strong></br>
            </div>
        
        </div>
    </div>
    ';

    echo $html;
    } else {
        echo  'sentiment api is off.';
    }
}

add_action( 'init', 'my_template_hooks', 5, 0 );

    function my_template_hooks(){

        /* load page theme */
        add_filter( 'comment_form_before', 'show_analize');

    }